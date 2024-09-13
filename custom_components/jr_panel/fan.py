"""Platform for JR Panel fan integration."""
from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up JR Panel fans from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        JRPanelFan(coordinator, i+1)
        for i in range(coordinator.model.num_fans)
    )

class JRPanelFan(CoordinatorEntity, FanEntity):
    """Representation of a JR Panel Fan."""

    def __init__(self, coordinator, fan_id):
        """Initialize the fan."""
        super().__init__(coordinator)
        self._fan_id = fan_id
        self._attr_name = f"Fan {fan_id}"
        self._attr_unique_id = f"{coordinator.client.host}_fan_{fan_id}"
        self._attr_supported_features = FanEntityFeature.SET_SPEED

    @property
    def is_on(self):
        """Return true if fan is on."""
        return self.coordinator.data[f"fan_{self._fan_id}"] > 0

    @property
    def percentage(self):
        """Return the current speed percentage."""
        return self.coordinator.data[f"fan_{self._fan_id}"]

    async def async_turn_on(self, percentage=None, preset_mode=None, **kwargs):
        """Turn the fan on."""
        if percentage is None:
            percentage = 50
        await self.async_set_percentage(percentage)

    async def async_turn_off(self, **kwargs):
        """Turn the fan off."""
        await self.coordinator.client.set_fan(self._fan_id, 0)
        await self.coordinator.async_request_refresh()

    async def async_set_percentage(self, percentage):
        """Set the speed of the fan."""
        await self.coordinator.client.set_fan(self._fan_id, percentage)
        await self.coordinator.async_request_refresh()
