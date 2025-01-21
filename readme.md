<p align="center">
  <img src="https://raw.githubusercontent.com/youkorr/hacs-jpg-to-png-converter/main/custom_components/jpg_to_png_converter/images/logo.png" alt="JPG to PNG Converter" width="400"/>
</p>

# JPG to PNG Converter for Home Assistant

A Home Assistant integration that converts JPG images to PNG format with customizable resolutions and optimization for ESP32 devices.

## Features
- Convert JPG images to PNG format
- Multiple resolution options
- ESP32 optimization mode (256 colors)
- Standard optimization mode (128 colors for smaller file size)
- Automatic output directory creation
- Optimized PNG output

## Prerequisites
The integration will automatically install required dependencies:
- Pillow (Python Imaging Library)

## Compatible Devices
- ESP32 (optimized with 256 colors mode)
- Any device that can display PNG images
- Home Assistant compatible cameras

## Installation

### Through Home Assistant UI
1. Go to Settings > Devices & Services
2. Click "Add Integration"
3. Search for "JPG to PNG"
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
12. Search for "JPG to PNG"
13. Follow the configuration steps

## Usage

### Service
The integration provides a service `jpg_to_png_converter.convert` with the following parameters:

```yaml
service: jpg_to_png_converter.convert
data:
  input_path: "/config/www/image.jpg"
  output_path: "/config/www/image.png"
  resolution: "original"
  optimize_mode: "esp32"  # Options: "none", "esp32", "standard"
```

### Parameters
- `input_path`: Path to the input JPG file (required)
- `output_path`: Path where the PNG file should be saved (optional)
- `resolution`: Output resolution (optional, defaults to "320x240")
  - Available options: "original","100x100", "200x200", "320x240", "640x480", "800x600", "1280x720", "1920x1080"
- `optimize_mode`: Optimization mode (optional, defaults to "none")
  - "none": No color optimization
  - "esp32": ESP32 mode with 256 colors (best for ESP32 displays)
  - "standard": 128 colors optimization for smaller file size

### Example Automations

#### Convert for ESP32 Display
```yaml
automation:
  - alias: "Convert for ESP32 Display"
    trigger:
      - platform: time_pattern
        minutes: "/5"
    action:
      - service: jpg_to_png_converter.convert
        data:
          input_path: "/config/www/source.jpg"
          output_path: "/config/www/esp32/display.png"
          resolution: "original"
          optimize_mode: "esp32"  # Use ESP32 mode for 256 colors
```

#### Convert with Size Optimization
```yaml
automation:
  - alias: "Convert with Size Optimization"
    trigger:
      - platform: state
        entity_id: binary_sensor.camera_motion
        to: "on"
    action:
      - service: jpg_to_png_converter.convert
        data:
          input_path: "/config/www/camera_image.jpg"
          output_path: "/config/www/converted/image.png"
          resolution: "original"
          optimize_mode: "standard"  # Use standard mode for smaller file size
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

