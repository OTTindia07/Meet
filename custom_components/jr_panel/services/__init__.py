"""Services for JR Touch Panel."""



"""Abstract service for JR Touch Panel entities."""
from abc import ABC, abstractmethod

class AbstractService(ABC):
    """Abstract service for JR Touch Panel entities."""

    def __init__(self, accessory, dp_id):
        """Initialize the service."""
        self.accessory = accessory
        self.dp_id = dp_id

    @abstractmethod
    async def update(self):
        """Update the entity state."""

    @abstractmethod
    async def set_state(self, value):
        """Set the entity state."""
