# JPG to PNG Converter - Home Assistant Integration

Convert JPG images to PNG format directly from Home Assistant using this custom integration.
## Features
- Convert JPG images to PNG format
- Multiple resolution options:
  - 320x240 (default)
  - 640x480
  - 800x600
  - 1280x720
  - 1920x1080
  - original (keeps original size)
- Automatic output directory creation
- Optimized PNG output

## Features
- Convert JPG images to PNG format
- Simple service call with `source_path` and `destination_path`
- Lightweight and easy to use
- Integration with Home Assistant events
- Compatible with Frigate and other image sources

# JPG to PNG Converter for Home Assistant

A Home Assistant integration that converts JPG images to PNG format with customizable resolutions.

## Features
- Convert JPG images to PNG format
- Multiple resolution options:
  - 320x240 (default)
  - 640x480
  - 800x600
  - 1280x720
  - 1920x1080
  - original (keeps original size)
- Automatic output directory creation
- Optimized PNG output

## Installation

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

## Usage

### Service
The integration provides a service `jpg_to_png_converter.convert` with the following parameters:

```yaml
service: jpg_to_png_converter.convert
data:
  input_path: "/config/www/image.jpg"
  output_path: "/config/www/image.png"
  resolution: "1280x720"
```
### Example Automation
```yaml
automation:
  - alias: "Convert Camera Image"
    trigger:
      - platform: state
        entity_id: camera.front_door
    action:
      - service: jpg_to_png_converter.convert
        data:
          input_path: "/config/www/camera_image.jpg"
          output_path: "/config/www/converted/image.png"
          resolution: "1280x720"
```

### Parameters
- `input_path`: Path to the input JPG file (required)
- `output_path`: Path where the PNG file should be saved (optional)
- `resolution`: Output resolution (optional, defaults to "320x240")


```

## Requirements
- [Pillow](https://pypi.org/project/Pillow/) Python library (installed automatically if missing)
- Home Assistant 2024.1.0 or newer

## Support
If you encounter any issues or have suggestions, please [open an issue](https://github.com/youkorr/hacs-jpg-to-png-converter/issues).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
