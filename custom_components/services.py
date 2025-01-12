"""Services for JPG to PNG Converter."""
import os
from PIL import Image
from homeassistant.core import HomeAssistant, ServiceCall

async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for JPG to PNG Converter."""
    
    async def convert_jpg_to_png(call: ServiceCall) -> None:
        """Handle the service call."""
        input_path = call.data.get("input_path")
        output_path = call.data.get("output_path", None)
        
        if not output_path:
            output_path = os.path.splitext(input_path)[0] + ".png"
            
        try:
            img = Image.open(input_path)
            img.save(output_path, "PNG")
        except Exception as e:
            raise Exception(f"Error converting image: {str(e)}")

    hass.services.async_register(
        "jpg_to_png_converter", 
        "convert", 
        convert_jpg_to_png
    )
