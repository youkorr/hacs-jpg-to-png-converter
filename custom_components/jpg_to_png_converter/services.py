import os
import tempfile
import aiohttp
import re
import cv2  # Ajout d'OpenCV pour capturer RTSP
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

def parse_custom_resolution(resolution_str: str) -> tuple:
    """Parse custom resolution string in format WIDTHxHEIGHT."""
    pattern = r'^(\d+)x(\d+)$'
    match = re.match(pattern, resolution_str)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None

async def download_image(url: str) -> str:
    """Download image from URL using aiohttp and return temporary file path."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        tmp_file.write(chunk)
                    return tmp_file.name
    except Exception as e:
        _LOGGER.error(f"Failed to download image: {str(e)}")
        raise

async def capture_rtsp_frame(rtsp_url: str) -> str:
    """Capture une image depuis un flux RTSP et retourner le chemin du fichier temporaire."""
    try:
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            raise Exception("Impossible d'ouvrir le flux RTSP")
        
        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise Exception("Échec de la capture d'image depuis RTSP")

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        cv2.imwrite(temp_file.name, frame)
        return temp_file.name
    except Exception as e:
        _LOGGER.error(f"Erreur RTSP: {str(e)}")
        raise

def process_image(input_path: str, output_path: str, resolution: str, optimize_mode: str) -> None:
    """Process and convert image to PNG."""
    try:
        _LOGGER.debug(f"Opening image from {input_path}")
        with Image.open(input_path) as img:
            if img.format in ['WEBP', 'JPEG', 'JPG']:
                img = img.convert('RGB')

            # Redimensionnement
            if resolution != "original":
                target_size = RESOLUTIONS.get(resolution) or parse_custom_resolution(resolution)
                if target_size:
                    img = img.resize(target_size, Image.Resampling.LANCZOS)
                    _LOGGER.debug(f"Resizing image to {resolution} ({target_size[0]}x{target_size[1]})")

            # Optimisation
            if optimize_mode == "esp32":
                img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
            elif optimize_mode == "standard":
                img = img.convert("P", palette=Image.ADAPTIVE, colors=128)
                img = img.quantize(colors=128, method=2)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path, format="PNG", optimize=True, compress_level=9)

            _LOGGER.info(f"Converted {input_path} to {output_path}")

    except Exception as e:
        _LOGGER.error(f"Error processing image: {str(e)}")
        raise

async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for JPG to PNG Converter."""

    async def convert_image(call: ServiceCall) -> None:
        """Handle the service call."""
        local_input_path = call.data.get("local_input_path")
        url_input_path = call.data.get("url_input_path")
        rtsp_input_url = call.data.get("rtsp_input_url")  # <-- Nouveau paramètre RTSP
        output_path = call.data.get("output_path")
        resolution = call.data.get("resolution", "320x240")
        custom_resolution = call.data.get("custom_resolution")
        optimize_mode = call.data.get("optimize_mode", "none")

        if custom_resolution:
            resolution = custom_resolution

        if not local_input_path and not url_input_path and not rtsp_input_url:
            raise Exception("Un des paramètres 'local_input_path', 'url_input_path' ou 'rtsp_input_url' est requis")

        temp_file = None
        try:
            if rtsp_input_url:
                temp_file = await capture_rtsp_frame(rtsp_input_url)
                input_path = temp_file
            elif url_input_path:
                temp_file = await download_image(url_input_path)
                input_path = temp_file
            else:
                input_path = local_input_path
                if not os.path.exists(input_path):
                    raise FileNotFoundError(f"Fichier introuvable: {input_path}")

            await hass.async_add_executor_job(
                process_image, input_path, output_path, resolution, optimize_mode
            )

        finally:
            if temp_file and os.path.exists(temp_file):
                os.unlink(temp_file)

    hass.services.async_register(
        "jpg_to_png_converter", 
        "convert", 
        convert_image
    )

