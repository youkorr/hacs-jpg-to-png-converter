from PIL import Image
    from homeassistant.core import ServiceCall

    async def async_convert_jpg_to_png(call: ServiceCall):
        """Handle the service call to convert JPG to PNG."""
        source = call.data.get('source_path')
        destination = call.data.get('destination_path')
        
        try:
            img = Image.open(source)
            img.save(destination, 'PNG')
            return True
        except Exception as e:
            raise Exception(f"Conversion failed: {str(e)}")
