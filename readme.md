<p align="center">
  <img src="https://raw.githubusercontent.com/youkorr/hacs-jpg-to-png-converter/main/custom_components/jpg_to_png_converter/images/logo.png" alt="JPG/WebP to PNG Converter" width="400"/>
</p>

# JPG/WebP to PNG Converter for Home Assistant

A Home Assistant integration that converts JPG/JPEG/WebP images to PNG format with customizable resolutions and optimization modes.

## Features
- Convert JPG/JPEG and WebP images to PNG format
- Support for local files and remote URLs
- Multiple resolution options
- ESP32 optimization mode (256 colors)
- Standard optimization mode (128 colors for smaller file size)
- Automatic output directory creation
- Optimized PNG output
- Asynchronous downloads for remote URLs

## Prerequisites
The integration will automatically install required dependencies:
- Pillow (Python Imaging Library)
- aiohttp (for asynchronous HTTP requests)

## Compatible Devices
- ESP32 (optimized with 256 colors mode)
- Any device that can display PNG images
- Home Assistant compatible cameras

## Installation

### Through Home Assistant UI
1. Go to Settings > Devices & Services
2. Click "Add Integration"
3. Search for "JPG/WebP to PNG"
4. Follow the configuration steps

### HACS Installation
1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/youkorr/hacs-jpg-to-png-converter`
6. Select "Integration" as the category
7. Click "Add"
8. Install the integration through HACS
9. Restart Home Assistant
10. Go to Settings > Devices & Services
11. Click "Add Integration"
12. Search for "JPG/WebP to PNG"
13. Follow the configuration steps

## Usage

### Service
The integration provides a service `jpg_to_png_converter.convert` with the following parameters:

```yaml
service: jpg_to_png_converter.convert
data:
  local_input_path: "/config/www/image.jpg"  # For local files
  url_input_path: "https://example.com/image.webp"  # For remote URLs
  output_path: "/config/www/converted.png"
  resolution: "original"  # Options: "original", "320x240", "640x480", etc.
  optimize_mode: "standard"  # Options: "none", "esp32", "standard"
```

### Examples

#### Local JPG/JPEG Conversion
```yaml
service: jpg_to_png_converter.convert
data:
  local_input_path: "/config/www/image.jpg"
  output_path: "/config/www/converted.png"
  resolution: "original"
  optimize_mode: "none"
```

#### Local WebP Conversion
```yaml
service: jpg_to_png_converter.convert
data:
  local_input_path: "/config/www/image.webp"
  output_path: "/config/www/converted.png"
  resolution: "640x480"
  optimize_mode: "standard"
```

#### Remote JPG/JPEG Conversion
```yaml
service: jpg_to_png_converter.convert
data:
  url_input_path: "https://example.com/image.jpg"
  output_path: "/config/www/converted.png"
  resolution: "1920x1080"
  optimize_mode: "esp32"
```

#### Remote WebP Conversion
```yaml
service: jpg_to_png_converter.convert
data:
  url_input_path: "https://example.com/image.webp"
  output_path: "/config/www/converted.png"
  resolution: "original"
  optimize_mode: "standard"
```

### Example Automations

#### Convert Local JPG for ESP32 Display
```yaml
automation:
  - alias: "Convert Local JPG for ESP32 Display"
    trigger:
      - platform: time_pattern
        minutes: "/5"
    action:
      - service: jpg_to_png_converter.convert
        data:
          local_input_path: "/config/www/source.jpg"
          output_path: "/config/www/esp32/display.png"
          resolution: "original"
          optimize_mode: "esp32"
```

#### Convert Remote WebP with Size Optimization
```yaml
automation:
  - alias: "Convert Remote WebP with Size Optimization"
    trigger:
      - platform: state
        entity_id: binary_sensor.camera_motion
        to: "on"
    action:
      - service: jpg_to_png_converter.convert
        data:
          url_input_path: "https://example.com/camera_image.webp"
          output_path: "/config/www/converted/image.png"
          resolution: "original"
          optimize_mode: "standard"
```

## Optimization Modes
- **ESP32 Mode**: Uses 256 colors, optimized for ESP32 displays. Best for maintaining image quality on ESP32 devices.
- **Standard Mode**: Uses 128 colors with additional compression. Best for reducing file size while maintaining acceptable quality.

## Troubleshooting
- Make sure the input path exists and is accessible
- Ensure Home Assistant has write permissions to the output directory
- Check Home Assistant logs for detailed error messages
- For ESP32 devices, use optimize_mode: "esp32" with resolution: "original"
- For smaller file sizes, use optimize_mode: "standard"

## Support
For bugs or feature requests, please open an issue on GitHub.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

