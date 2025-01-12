from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

DOMAIN = "jpg_to_png"

class JpgToPngConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JPG to PNG Converter."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        return self.async_create_entry(title="JPG to PNG Converter", data={})

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "jpg_to_png")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    return True

