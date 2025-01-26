"""Services for JPG to PNG Converter."""
import os
import tempfile
import requests
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

def download_image(url: str) -> str:
    """Download image from URL using requests and return temporary file path."""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
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
            # Convert to RGB if needed
            if img.format in ['WEBP', 'JPEG', 'JPG']:
                img = img.convert('RGB')
            
            # Resize if needed
            if resolution != "original" and resolution in RESOLUTIONS:
                target_size = RESOLUTIONS[resolution]
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
        
        if not local_input_path and not url_input_path:
            raise Exception("Either local_input_path or url_input_path must be provided")
        
        temp_file = None
        try:
            if url_input_path:
                temp_file = download_image(url_input_path)
                input_path = temp_file
            else:
                input_path = local_input_path
                if not os.path.exists(input_path):
                    raise Exception(f"Input file not found: {input_path}")
            
            process_image(input_path, output_path, resolution, optimize_mode)
            
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
