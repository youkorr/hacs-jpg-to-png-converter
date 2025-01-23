"""Config flow for JPG to PNG Converter integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

class JPGToPNGConverterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JPG to PNG Converter."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({})
            )

        return self.async_create_entry(title="JPG to PNG Converter", data={})
