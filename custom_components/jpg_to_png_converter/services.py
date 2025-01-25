"""Services for JPG to PNG Converter."""
import os
import requests
from PIL import Image
import logging
from homeassistant.core import HomeAssistant, ServiceCall
from io import BytesIO

LOGGER = logging.getLogger(__name__)

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
        
        # Process local files
        for input_path in local_input_paths:
            output_path = call.data.get("output_path")
            resolution = call.data.get("resolution", "320x240")
            optimize_mode = call.data.get("optimize_mode", "none")
            
            if input_path.lower().endswith(('.jpg', '.jpeg', '.webp')):
                try:
                    # Open the image
                    img = Image.open(input_path)
                    
                    # Resize if a specific resolution is requested
                    if resolution != "original" and RESOLUTIONS.get(resolution):
                        img = img.resize(RESOLUTIONS[resolution], Image.LANCZOS)
                    
                    # Determine output path if not provided
                    if not output_path:
                        output_path = os.path.splitext(input_path)[0] + ".png"
                    
                    # Save the image as PNG
                    img.save(output_path, "PNG")
                    LOGGER.info(f"Converted {input_path} to {output_path}")
                
                except Exception as e:
                    LOGGER.error(f"Error converting local image {input_path}: {str(e)}")
                    raise
        
        # Process URL-based files
        for input_path in url_input_paths:
            output_path = call.data.get("output_path")
            resolution = call.data.get("resolution", "320x240")
            optimize_mode = call.data.get("optimize_mode", "none")
            
            try:
                # Download image from URL
                LOGGER.debug(f"Downloading image from URL: {input_path}")
                response = requests.get(input_path)
                response.raise_for_status()
                
                # Open image from downloaded content
                img = Image.open(BytesIO(response.content))
                
                # Resize if a specific resolution is requested
                if resolution != "original" and RESOLUTIONS.get(resolution):
                    img = img.resize(RESOLUTIONS[resolution], Image.LANCZOS)
                
                # Determine output path if not provided
                if not output_path:
                    url_filename = input_path.split('/')[-1]
                    base_name = os.path.splitext(url_filename)[0]
                    output_path = os.path.join(hass.config.media_dir, f"{base_name}.png")
                
                # Save the image as PNG
                img.save(output_path, "PNG")
                LOGGER.info(f"Converted URL image {input_path} to {output_path}")
            
            except Exception as e:
                LOGGER.error(f"Error converting URL image {input_path}: {str(e)}")
                raise

    # Register the service with Home Assistant
    hass.services.async_register(
        "jpg_to_png_converter", 
        "convert", 
        convert_jpg_to_png
    )

