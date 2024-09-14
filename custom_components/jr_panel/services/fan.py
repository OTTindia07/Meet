"""Fan service for JR Touch Panel."""
from homeassistant.components.fan import FanEntity, SUPPORT_SET_SPEED
from homeassistant.util.percentage import (
    int_states_in_range,
    percentage_to_ranged_value,
    ranged_value_to_percentage,
)

from .abstract_service import AbstractService

class JRFan(FanEntity, AbstractService):
    """Representation of a JR Touch Panel fan."""

    @property
    def is_on(self):
        """Return true if the fan is on."""
        return self.accessory.entities[self.dp_id]["value"] > 0

    @property
    def percentage(self):
        """Return the current speed percentage."""
        return ranged_value_to_percentage((0, 100), self.accessory.entities[self.dp_id]["value"])

    @property
    def speed_count(self):
        """Return the number of speeds the fan supports."""
        return int_states_in_range((0, 100))

    async def async_set_percentage(self, percentage):
        """Set the speed of the fan."""
        if percentage == 0:
            await self.async_turn_off()
        else:
            await self.set_state(percentage_to_ranged_value((0, 100), percentage))

    async def async_turn_on(self, **kwargs):
        """Turn the fan on."""
        await self.set_state(25)  # Set to 25% speed when turning on

    async def async_turn_off(self, **kwargs):
        """Turn the fan off."""
        await self.set_state(0)

    async def update(self):
        """Update the fan state."""
        self.accessory.entities[self.dp_id]["value"] = await self.accessory.get_state(self.dp_id)

    async def set_state(self, value):
        """Set the fan state."""
        await self.accessory.set_state(self.dp_id, value)
        self.accessory.entities[self.dp_id]["value"] = value
