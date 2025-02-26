"""Services for JPG to PNG Converter."""
import os
import tempfile
import aiohttp
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

def process_image(input_path: str, output_path: str, resolution: str, optimize_mode: str, zoom_mode: str = "fit") -> None:
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
            if resolution != "original" and resolution in RESOLUTIONS:
                target_size = RESOLUTIONS[resolution]
                
                # Handling zoom mode to preserve aspect ratio
                if zoom_mode == "zoom":
                    original_width, original_height = img.size
                    target_width, target_height = target_size
                    
                    # Calculate aspect ratios
                    original_ratio = original_width / original_height
                    target_ratio = target_width / target_height
                    
                    # Determine dimensions to maintain aspect ratio
                    if original_ratio > target_ratio:
                        # Original is wider than target
                        new_height = target_height
                        new_width = int(new_height * original_ratio)
                    else:
                        # Original is taller than target
                        new_width = target_width
                        new_height = int(new_width / original_ratio)
                    
                    # Resize while maintaining aspect ratio
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Create a new image with target size and paste resized image centered
                    new_img = Image.new('RGB', target_size, (0, 0, 0))
                    paste_x = (target_width - new_width) // 2
                    paste_y = (target_height - new_height) // 2
                    new_img.paste(img, (paste_x, paste_y))
                    img = new_img
                    
                    _LOGGER.debug(f"Resizing image with zoom mode to {resolution} (aspect ratio preserved)")
                else:
                    # Standard resize (fit mode)
                    img = img.resize(target_size, Image.Resampling.LANCZOS)
                    _LOGGER.debug(f"Resizing image to {resolution}")
            
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
        optimize_mode = call.data.get("optimize_mode", "none")
        zoom_mode = call.data.get("zoom_mode", "fit")
        
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
                process_image, input_path, output_path, resolution, optimize_mode, zoom_mode
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
