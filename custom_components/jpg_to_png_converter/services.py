"""Services for JPG to PNG Converter."""
import os
from PIL import Image
import logging
from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for JPG to PNG Converter."""
    
    async def convert_jpg_to_png(call: ServiceCall) -> None:
        """Handle the service call."""
        input_path = call.data.get("input_path")
        output_path = call.data.get("output_path", None)
        
        if not output_path:
            output_path = os.path.splitext(input_path)[0] + ".png"
            
        try:
            # Check if input file exists
            if not os.path.exists(input_path):
                raise Exception(f"Input file not found: {input_path}")
                
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Open and convert image
            _LOGGER.debug(f"Opening image from {input_path}")
            img = Image.open(input_path)
            
            _LOGGER.debug(f"Saving image to {output_path}")
            img.save(output_path, "PNG")
            _LOGGER.info(f"Successfully converted {input_path} to {output_path}")
            
        except Exception as e:
            _LOGGER.error(f"Error converting image: {str(e)}")
            raise Exception(f"Error converting image: {str(e)}")

    hass.services.async_register(
        "jpg_to_png_converter", 
        "convert", 
        convert_jpg_to_png
    )
