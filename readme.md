# JPG to PNG Converter - Home Assistant Integration

Convert JPG images to PNG format directly from Home Assistant using this custom integration.

## Features
- Convert JPG images to PNG format
- Simple service call with `source_path` and `destination_path`
- Lightweight and easy to use
- Integration with Home Assistant events
- Compatible with Frigate and other image sources

## Installation

### Via HACS (Recommended)
1. Go to **HACS** > **Integrations** in your Home Assistant.
2. Click on the three dots in the top-right corner and select **Custom repositories**.
3. Add this repository URL: `https://github.com/youkorr/hacs-jpg-to-png-converter`.
4. Select **Integration** as the category.
5. Click **Add** and then **Install**.

### Manual Installation
1. Download the `custom_components/jpg_to_png` folder from this repository.
2. Place the `jpg_to_png` folder in your Home Assistant `custom_components` directory.
3. Restart Home Assistant.

## Usage
After installation, you can use the `convert_jpg_to_png` service in Home Assistant.

### Service Call
```yaml
service: jpg_to_png.convert_jpg_to_png
data:
  source_path: "/config/www/images/input.jpg"
  destination_path: "/config/www/images/output.png"
```

### Example Automations

#### Basic File Conversion
```yaml
automation:
  - alias: Convert JPG to PNG on File Creation
    trigger:
      - platform: event
        event_type: file_created
        event_data:
          path: "/config/www/images/input.jpg"
    action:
      - service: jpg_to_png.convert_jpg_to_png
        data:
          source_path: "/config/www/images/input.jpg"
          destination_path: "/config/www/images/output.png"
```

#### Frigate Integration Example
```yaml
automation:
  - alias: Convert JPG to PNG on File Creation
    trigger:
      - platform: event
        event_type: file_created
        event_data:
          path: "/config/www/llmvision/frigate1.jpg"
    action:
      - service: jpg_to_png.convert_jpg_to_png
        data:
          source_path: "/config/www/llmvision/frigate1.jpg"
          destination_path: "/config/www/llmvision/frigate1.png"
```

## Requirements
- [Pillow](https://pypi.org/project/Pillow/) Python library (installed automatically if missing)
- Home Assistant 2024.1.0 or newer

## Support
If you encounter any issues or have suggestions, please [open an issue](https://github.com/youkorr/hacs-jpg-to-png-converter/issues).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.