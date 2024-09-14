"""Config flow for JR Touch Panel integration."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_PORT, DOMAIN
from .discovery import discover_jr_panels
from .jr_accessory import JRAccessory

_LOGGER = logging.getLogger(__name__)

class JRPanelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JR Touch Panel."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                accessory = JRAccessory(self.hass, user_input)
                await accessory.connect()
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_NAME): str,
                    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                }
            ),
            errors=errors,
        )

    async def async_step_zeroconf(self, discovery_info):
        """Handle zeroconf discovery."""
        # Implement zeroconf discovery logic here
        pass
