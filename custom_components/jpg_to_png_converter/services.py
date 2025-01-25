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
        # Handle local files
        if "local_input_path" in call.data:
            input_path = call.data["local_input_path"]
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

            # Process image based on resolution and optimization
            if resolution != "original":
                img = img.resize(RESOLUTIONS[resolution])

            # Save the processed image
            img.save(output_path, optimize=(optimize_mode != "none"))

        # Handle URL-based images
        elif "url_input_path" in call.data:
            input_url = call.data["url_input_path"]
            output_path = call.data.get("output_path", None)
            resolution = call.data.get("resolution", "320x240")
            optimize_mode = call.data.get("optimize_mode", "none")

            try:
                _LOGGER.debug(f"Downloading image from URL: {input_url}")
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(input_url, headers=headers)
                response.raise_for_status()

                # Open image with PIL
                img = Image.open(BytesIO(response.content))

                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background

                if not output_path:
                    url_filename = input_url.split('/')[-1].split('?')[0]
                    base_name = os.path.splitext(url_filename)[0]
                    output_path = os.path.join(hass.config.media_dir, f"{base_name}.png")

                # Process image based on resolution and optimization
                if resolution != "original":
                    img = img.resize(RESOLUTIONS[resolution])

                # Save the processed image
                img.save(output_path, optimize=(optimize_mode != "none"))

            except Exception as e:
                _LOGGER.error(f"Error converting image from URL: {str(e)}")
                raise Exception(f"Error converting image from URL: {str(e)}")
        else:
            raise Exception("Either local_input_path or url_input_path must be provided")

    hass.services.async_register(
        "jpg_to_png_converter", 
        "convert", 
        convert_jpg_to_png
    )

