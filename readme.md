<p align="center">
  <img src="https://raw.githubusercontent.com/youkorr/hacs-jpg-to-png-converter/main/custom_components/jpg_to_png_converter/images/logo.png" alt="JPG/WebP to PNG Converter" width="400"/>
</p>

# JPG/WebP to PNG Converter for Home Assistant

A Home Assistant integration that converts JPG/JPEG/WebP images to PNG format with customizable resolutions and optimization modes.

## Features
- Convert JPG/JPEG and WebP images to PNG format
- Support for local files and remote URLs
- Multiple resolution options (320x240, 640x480, 800x600, 1280x720, 1920x1080)
- Adjustable zoom modes: fit (stretch) or zoom (preserve aspect ratio)
- ESP32 optimization mode (256 colors)
- Standard optimization mode (128 colors for smaller file size)
- Automatic output directory creation
- Optimized PNG output
- Asynchronous downloads for remote URLs

## Prerequisites
The integration will automatically install required dependencies:
- Pillow (Python Imaging Library) >=9.0.0
- aiohttp (for asynchronous HTTP requests) >=3.8.0

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
  local_input_path: "/config/www/image.jpg"  # For local files (optional)
  url_input_path: "https://example.com/image.webp"  # For remote URLs (optional)
  output_path: "/config/www/converted.png"  # Required
  resolution: "original"  # Optional, default: "320x240"
  zoom_mode: "fit"  # Optional, default: "fit"
  optimize_mode: "none"  # Optional, default: "none"
```

#### Parameter Details

| Parameter | Description | Required | Default | Options |
|-----------|-------------|----------|---------|---------|
| `local_input_path` | Path to the local input JPG/WebP file | No | - | Any valid file path |
| `url_input_path` | URL of the remote JPG/WebP file | No | - | Any valid URL |
| `output_path` | Path where the PNG file should be saved | Yes | - | Any valid file path |
| `resolution` | Select output resolution | No | "320x240" | "original", "320x240", "640x480", "800x600", "1280x720", "1920x1080" |
| `zoom_mode` | Mode de redimensionnement | No | "fit" | "fit" (Adapter - étirement), "zoom" (Zoom - conserve les proportions) |
| `optimize_mode` | Choose optimization mode | No | "none" | "none", "esp32" (256 colors), "standard" (128 colors) |

### Examples

#### Local JPG/JPEG Conversion
```yaml
service: jpg_to_png_converter.convert
data:
  local_input_path: "/config/www/image.jpg"
  output_path: "/config/www/converted.png"
  resolution: "original"
  zoom_mode: "fit"
  optimize_mode: "none"
```

#### Local WebP Conversion with Aspect Ratio Preservation
```yaml
service: jpg_to_png_converter.convert
data:
  local_input_path: "/config/www/image.webp"
  output_path: "/config/www/converted.png"
  resolution: "640x480"
  zoom_mode: "zoom"  # Preserve aspect ratio
  optimize_mode: "standard"
```

#### Remote JPG/JPEG Conversion
```yaml
service: jpg_to_png_converter.convert
data:
  url_input_path: "https://example.com/image.jpg"
  output_path: "/config/www/converted.png"
  resolution: "1920x1080"
  zoom_mode: "fit"
  optimize_mode: "esp32"
```

#### Remote WebP Conversion
```yaml
service: jpg_to_png_converter.convert
data:
  url_input_path: "https://example.com/image.webp"
  output_path: "/config/www/converted.png"
  resolution: "original"
  zoom_mode: "zoom"  # Preserve aspect ratio
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
          zoom_mode: "zoom"  # Preserve aspect ratio
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
          resolution: "320x240"  # Reduce resolution for smaller file
          zoom_mode: "fit"
          optimize_mode: "standard"
```

## Optimization Modes
- **ESP32 Mode**: Uses 256 colors, optimized for ESP32 displays. Best for maintaining image quality on ESP32 devices.
- **Standard Mode**: Uses 128 colors with additional compression. Best for reducing file size while maintaining acceptable quality.

## Supported Formats
- JPG
- JPEG
- WebP

## Supported Features
- Local file conversion
- Remote URL conversion
- Resolution scaling with multiple preset options
- Aspect ratio preservation with zoom mode options
- Multiple optimization modes for different device types

## Integration Details
- Version: 1.6.0
- IoT Class: local_polling
- Icon: mdi:image-refresh
- Integration Type: service
- Config Flow: Yes

## Troubleshooting
- Make sure the input path exists and is accessible
- Ensure Home Assistant has write permissions to the output directory
- Check Home Assistant logs for detailed error messages
- For ESP32 devices, use optimize_mode: "esp32" with resolution: "original"
- For smaller file sizes, use optimize_mode: "standard"

## Support
For bugs or feature requests, please open an issue on GitHub at:
[https://github.com/youkorr/hacs-jpg-to-png-converter/issues](https://github.com/youkorr/hacs-jpg-to-png-converter/issues)

## Documentation
Full documentation is available at:
[https://github.com/youkorr/hacs-jpg-to-png-converter](https://github.com/youkorr/hacs-jpg-to-png-converter)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

