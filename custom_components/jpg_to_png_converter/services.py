"""Services for JPG to PNG Converter."""
import os
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

async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for JPG to PNG Converter."""
    
    async def convert_jpg_to_png(call: ServiceCall) -> None:
        """Handle the service call."""
        input_path = call.data.get("input_path")
        output_path = call.data.get("output_path", None)
        resolution = call.data.get("resolution", "320x240")
        optimize = call.data.get("optimize", False)
        
        if not output_path:
            output_path = os.path.splitext(input_path)[0] + ".png"
            
        try:
            # Check if input file exists
            if not os.path.exists(input_path):
                raise Exception(f"Input file not found: {input_path}")
            
            _LOGGER.debug(f"Opening image from {input_path}")
            img = Image.open(input_path)
            
            # Resize the image if resolution is specified and not original
            if resolution != "original" and resolution in RESOLUTIONS:
                target_size = RESOLUTIONS[resolution]
                img = img.resize(target_size)
                _LOGGER.debug(f"Resizing image to {resolution}")
            
            # Optimize image if requested
            if optimize:
                _LOGGER.debug("Optimizing image with 256 color palette")
                img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
            
            # Delete existing PNG if it exists
            if os.path.exists(output_path):
                _LOGGER.debug(f"Deleting old PNG file: {output_path}")
                os.remove(output_path)
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            _LOGGER.debug(f"Saving PNG image to {output_path}")
            img.save(output_path, "PNG", optimize=True)
            
            if os.path.exists(output_path):
                _LOGGER.info(f"Successfully converted {input_path} to {output_path} with resolution {resolution}")
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
