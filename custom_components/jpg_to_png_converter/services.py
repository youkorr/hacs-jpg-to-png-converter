"""Services for JPG to PNG Converter."""
import os
import tempfile
import aiohttp
import re
from PIL import Image
import logging
from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

RESOLUTIONS = {
    "320x240": (320, 240),
    "640x480": (640, 480),
    "800x600": (800, 600),
    "1280x720": (1280, 720),
    "1920x1080": (1920, 1080),
    "original": None
}

def parse_custom_resolution(resolution_str: str) -> tuple:
    """Parse custom resolution string in format WIDTHxHEIGHT."""
    pattern = r'^(\d+)x(\d+)$'
    match = re.match(pattern, resolution_str)
    if match:
        width = int(match.group(1))
        height = int(match.group(2))
        return (width, height)
    return None

async def download_image(url: str) -> str:
    """Download image from URL using aiohttp and return temporary file path."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as tmp_file:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        tmp_file.write(chunk)
                    return tmp_file.name
    except Exception as e:
        _LOGGER.error(f"Failed to download image: {str(e)}")
        raise Exception(f"Failed to download image: {str(e)}")

def process_image(input_path: str, output_path: str, resolution: str, optimize_mode: str) -> None:
    """Process and convert image to PNG."""
    try:
        _LOGGER.debug(f"Opening image from {input_path}")
        with Image.open(input_path) as img:
            # Force detection of WebP format
            if img.format is None and input_path.lower().endswith('.webp'):
                img.format = 'WEBP'
                _LOGGER.debug(f"Manually set format to WEBP for {input_path}")
            
            # Convert to RGB if needed
            if img.format in ['WEBP', 'JPEG', 'JPG']:
                img = img.convert('RGB')
            
            # Resize if needed
            if resolution != "original":
                # Check if it's a predefined resolution
                if resolution in RESOLUTIONS:
                    target_size = RESOLUTIONS[resolution]
                else:
                    # Try to parse as custom resolution
                    target_size = parse_custom_resolution(resolution)
                
                if target_size:
                    img = img.resize(target_size, Image.Resampling.LANCZOS)
                    _LOGGER.debug(f"Resizing image to {resolution} ({target_size[0]}x{target_size[1]})")
                else:
                    _LOGGER.warning(f"Invalid resolution format: {resolution}, using original size")
            
            # Apply optimization
            if optimize_mode == "esp32":
                _LOGGER.debug("Applying ESP32 optimization (256 colors)")
                img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
            elif optimize_mode == "standard":
                _LOGGER.debug("Applying standard optimization (128 colors)")
                img = img.convert("P", palette=Image.ADAPTIVE, colors=128)
                img = img.quantize(colors=128, method=2)
            
            # Create output directory if needed
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save with options
            save_options = {
                "format": "PNG",
                "optimize": True,
                "compress_level": 9
            }
            
            if optimize_mode == "standard":
                save_options["bits"] = 8
            
            img.save(output_path, **save_options)
            
            if not os.path.exists(output_path):
                raise Exception(f"Failed to save PNG file: {output_path}")
            
            original_size = os.path.getsize(input_path)
            converted_size = os.path.getsize(output_path)
            _LOGGER.info(f"Successfully converted {input_path} to {output_path}")
            _LOGGER.info(f"File sizes - Original: {original_size/1024:.1f}KB, Converted: {converted_size/1024:.1f}KB")
            
    except Exception as e:
        _LOGGER.error(f"Error processing image: {str(e)}")
        raise Exception(f"Error processing image: {str(e)}")

async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for JPG to PNG Converter."""
    
    async def convert_image(call: ServiceCall) -> None:
        """Handle the service call."""
        local_input_path = call.data.get("local_input_path")
        url_input_path = call.data.get("url_input_path")
        output_path = call.data.get("output_path")
        resolution = call.data.get("resolution", "320x240")
        custom_resolution = call.data.get("custom_resolution")
        optimize_mode = call.data.get("optimize_mode", "none")
        
        # Use custom_resolution if provided
        if custom_resolution:
            resolution = custom_resolution
        
        if not local_input_path and not url_input_path:
            raise Exception("Either local_input_path or url_input_path must be provided")
        
        temp_file = None
        try:
            if url_input_path:
                temp_file = await download_image(url_input_path)
                input_path = temp_file
            else:
                input_path = local_input_path
                if not os.path.exists(input_path):
                    _LOGGER.error(f"Input file not found: {input_path}")
                    raise FileNotFoundError(f"Input file not found: {input_path}")
            
            await hass.async_add_executor_job(
                process_image, input_path, output_path, resolution, optimize_mode
            )
            
        except FileNotFoundError as e:
            _LOGGER.error(f"File not found error: {str(e)}")
            raise
        except Exception as e:
            _LOGGER.error(f"Error during conversion: {str(e)}")
            raise
        finally:
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except Exception as e:
                    _LOGGER.warning(f"Failed to delete temporary file: {str(e)}")

    hass.services.async_register(
        "jpg_to_png_converter", 
        "convert", 
        convert_image
    )
