"""The JPG to PNG Converter integration."""
from __future__ import annotations

import logging
from PIL import Image

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)
DOMAIN = "jpg_to_png"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the JPG to PNG Converter component."""
    
    async def convert_jpg_to_png(call: ServiceCall) -> None:
        """Handle the service call."""
        source_path = call.data.get("source_path")
        destination_path = call.data.get("destination_path")

        try:
            # Convert image from JPG to PNG
            with Image.open(source_path) as img:
                img.save(destination_path, 'PNG')
            _LOGGER.info(f"Successfully converted {source_path} to {destination_path}")
        except Exception as e:
            _LOGGER.error(f"Error converting image: {str(e)}")

    hass.services.async_register(DOMAIN, "convert_jpg_to_png", convert_jpg_to_png)
    
    return True

