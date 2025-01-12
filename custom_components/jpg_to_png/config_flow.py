from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN

class JpgToPngConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JPG to PNG Converter."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="JPG to PNG Converter", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={"description": "No configuration required. Click Submit to continue."},
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return JpgToPngOptionsFlow(config_entry)

class JpgToPngOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for JPG to PNG Converter."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
            description_placeholders={"description": "No options available."},
        )
