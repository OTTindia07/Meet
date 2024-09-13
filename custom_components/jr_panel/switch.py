"""Platform for JR Panel switch integration."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up JR Panel switches from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        JRPanelSwitch(coordinator, i+1)
        for i in range(coordinator.model.num_switches)
    )

class JRPanelSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a JR Panel Switch."""

    def __init__(self, coordinator, switch_id):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._switch_id = switch_id
        self._attr_name = f"Switch {switch_id}"
        self._attr_unique_id = f"{coordinator.client.host}_switch_{switch_id}"

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self.coordinator.data[f"switch_{self._switch_id}"]

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self.coordinator.client.set_switch(self._switch_id, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self.coordinator.client.set_switch(self._switch_id, False)
        await self.coordinator.async_request_refresh()
