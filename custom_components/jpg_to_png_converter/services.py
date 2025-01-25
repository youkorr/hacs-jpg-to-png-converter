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
    async def convert_jpg_to_png(call: ServiceCall) -> None:
        local_input_paths = call.data.get("local_input_path", [])
        url_input_paths = call.data.get("url_input_path", [])

        for input_path in local_input_paths:
            output_path = call.data.get("output_path", None)
            resolution = call.data.get("resolution", "320x240")
            optimize_mode = call.data.get("optimize_mode", "none")

            if input_path.endswith(('.jpg', '.jpeg', '.webp')):
                if input_path.endswith('.webp'):
                    _LOGGER.debug(f"Opening WEBP image from {input_path}")
                    img = Image.open(input_path)
                    output_path = os.path.splitext(input_path)[0] + ".png"
                else:
                    _LOGGER.debug(f"Opening JPG/JPEG image from {input_path}")
                    img = Image.open(input_path)
                    if not output_path:
                        output_path = os.path.splitext(input_path)[0] + ".png"
            else:
                raise Exception(f"Unsupported file type: {input_path}")

            # Rest of the local file processing logic

        for input_path in url_input_paths:
            output_path = call.data.get("output_path", None)
            resolution = call.data.get("resolution", "320x240")
            optimize_mode = call.data.get("optimize_mode", "none")

            try:
                _LOGGER.debug(f"Downloading image from URL: {input_path}")
                response = requests.get(input_path)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))

                if not output_path:
                    url_filename = input_path.split('/')[-1]
                    base_name = os.path.splitext(url_filename)[0]
                    output_path = os.path.join(hass.config.media_dir, f"{base_name}.png")

                # Rest of the URL-based processing logic
            except Exception as e:
                _LOGGER.error(f"Error converting image: {str(e)}")
                raise Exception(f"Error converting image: {str(e)}")

    hass.services.async_register(
        "jpg_to_png_converter", 
        "convert", 
        convert_jpg_to_png
    )
