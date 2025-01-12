"""The JPG to PNG Converter integration."""
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.typing import ConfigType

    DOMAIN = "jpg_to_png"

    async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
        """Set up the JPG to PNG Converter component."""
        return True
