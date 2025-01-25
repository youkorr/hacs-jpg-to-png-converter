"""Services for JPG to PNG Converter."""
import os
import requests
from PIL import Image
import logging
from homeassistant.core import HomeAssistant, ServiceCall
from io import BytesIO

_LOGGER = logging.getLogger(__name__)

RESOLUTIONS = {
    "100x100": (100, 100),
    "200x200": (200, 200),
    "320x240": (320, 240),
    "640x480": (640, 480),
    "800x600": (800, 600),
    "1280x720": (1280, 720),
    "1920x1080": (1920, 1080),
    "original": None
}

async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for JPG to PNG Converter."""
    
    async def convert_jpg_to_png(call: ServiceCall) -> None:
        """Handle the service call."""
        input_paths = call.data.get("input_path", [])  # Support for multiple paths/URLs
        
        # Ensure input_paths is a list
        if not isinstance(input_paths, list):
            input_paths = [input_paths]
        
        for input_path in input_paths:
            output_path = call.data.get("output_path", None)
            resolution = call.data.get("resolution", "320x240")
            optimize_mode = call.data.get("optimize_mode", "none")
            
            try:
                # Check if input is a URL
                if input_path.startswith(('http://', 'https://')):
                    _LOGGER.debug(f"Downloading image from URL: {input_path}")
                    try:
                        response = requests.get(input_path)
                        response.raise_for_status()
                        img = Image.open(BytesIO(response.content))
                    except Exception as e:
                        _LOGGER.error(f"Error downloading image from URL: {e}")
                        raise Exception(f"Error downloading image from URL: {e}")
                    
                    # Generate default output filename for URL images
                    if not output_path:
                        url_filename = input_path.split('/')[-1]
                        base_name = os.path.splitext(url_filename)[0]
                        output_path = os.path.join(hass.config.media_dir, f"{base_name}.png")
                
                else:
                    # Local file processing
                    if not os.path.exists(input_path):
                        raise Exception(f"Input file not found: {input_path}")
                    
                    _LOGGER.debug(f"Opening image from {input_path}")
                    img = Image.open(input_path)
                    
                    # Default output path for local files
                    if not output_path:
                        output_path = os.path.splitext(input_path)[0] + ".png"
                
                # Convert to RGB first to ensure proper color handling
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize first if needed
                if resolution != "original" and resolution in RESOLUTIONS:
                    target_size = RESOLUTIONS[resolution]
                    img = img.resize(target_size, Image.Resampling.BILINEAR)
                    _LOGGER.debug(f"Resizing image to {resolution}")
                
                # Apply optimization based on mode
                if optimize_mode == "esp32":
                    _LOGGER.debug("Applying ESP32 optimization (256 colors)")
                    img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
                elif optimize_mode == "standard":
                    _LOGGER.debug("Applying standard optimization (128 colors)")
                    img = img.convert("P", palette=Image.ADAPTIVE, colors=128)
                
                # Delete existing PNG if it exists
                if os.path.exists(output_path):
                    _LOGGER.debug(f"Deleting old PNG file: {output_path}")
                    os.remove(output_path)
                
                # Create output directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                _LOGGER.debug(f"Saving PNG image to {output_path}")
                # Optimized save settings
                save_options = {
                    "format": "PNG",
                    "optimize": True,
                    "compress_level": 6
                }
                
                img.save(output_path, **save_options)
                
                if os.path.exists(output_path):
                    # Log file size for URL and local images
                    try:
                        original_size = response.headers.get('Content-Length', 0) if input_path.startswith(('http://', 'https://')) else os.path.getsize(input_path)
                    except:
                        original_size = 0
                    
                    converted_size = os.path.getsize(output_path)
                    _LOGGER.info(f"Successfully converted {input_path} to {output_path}")
                    _LOGGER.info(f"File sizes - Original: {float(original_size)/1024:.1f}KB, Converted: {converted_size/1024:.1f}KB")
                else:
                    raise Exception(f"PNG file was not saved: {output_path}")
                
            except Exception as e:
                _LOGGER.error(f"Error converting image: {str(e)}")
                raise Exception(f"Error converting image: {str(e)}")

    hass.services.async_register(
        "jpg_to_png_converter", 
        "convert", 
        convert_jpg_to_png
    )
