"""Services for JPG to PNG Converter."""
import os
from PIL import Image
import logging
from homeassistant.core import HomeAssistant, ServiceCall

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
        input_paths = call.data.get("input_path")
        
        # Assurez-vous que input_paths est une liste
        if not isinstance(input_paths, list):
            input_paths = [input_paths]
        
        for input_path in input_paths:
            # Ajout du support explicite pour .jpg et .jpeg
            if not (input_path.lower().endswith(('.jpg', '.jpeg')) and os.path.exists(input_path)):
                _LOGGER.error(f"Invalid or non-existent file: {input_path}")
                continue

            output_path = call.data.get("output_path", None)
            resolution = call.data.get("resolution", "320x240")
            optimize_mode = call.data.get("optimize_mode", "none")
            
            if not output_path:
                output_path = os.path.splitext(input_path)[0] + ".png"
                
            try:
                _LOGGER.debug(f"Opening image from {input_path}")
                img = Image.open(input_path)
                
                # Reste du code inchangé
                # ... (le code précédent reste identique)

    hass.services.async_register(
        "jpg_to_png_converter", 
        "convert", 
        convert_jpg_to_png
    )
