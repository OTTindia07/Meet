"""Config flow for JR Panel integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN
from .discovery import discover_jr_panels

class JRPanelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JR Panel."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            discovered_panels = await discover_jr_panels()
            if discovered_panels:
                return await self.async_step_discovery()
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_HOST): str,
                }),
            )

        await self.async_set_unique_id(user_input[CONF_HOST])
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

    async def async_step_discovery(self, user_input=None) -> FlowResult:
        """Handle discovery step."""
        discovered_panels = await discover_jr_panels()
        if user_input is None:
            return self.async_show_form(
                step_id="discovery",
                data_schema=vol.Schema({
                    vol.Required("selected_panel"): vol.In({panel["host"]: panel["name"] for panel in discovered_panels}),
                }),
            )

        selected_panel = next(panel for panel in discovered_panels if panel["host"] == user_input["selected_panel"])
        await self.async_set_unique_id(selected_panel["host"])
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=selected_panel["name"], data=selected_panel)
