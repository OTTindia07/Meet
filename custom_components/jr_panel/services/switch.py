
"""Switch service for JR Touch Panel."""
from homeassistant.components.switch import SwitchEntity

from .abstract_service import AbstractService

class JRSwitch(SwitchEntity, AbstractService):
    """Representation of a JR Touch Panel switch."""

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.accessory.entities[self.dp_id]["value"]

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self.set_state(True)

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self.set_state(False)

    async def update(self):
        """Update the switch state."""
        self.accessory.entities[self.dp_id]["value"] = await self.accessory.get_state(self.dp_id)

    async def set_state(self, value):
        """Set the switch state."""
        await self.accessory.set_state(self.dp_id, value)
        self.accessory.entities[self.dp_id]["value"] = value
