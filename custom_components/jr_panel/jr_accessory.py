"""JR Touch Panel accessory."""
from homeassistant.const import CONF_HOST, CONF_PORT

from .tcp_client import TCPClient

class JRAccessory:
    """Representation of a JR Touch Panel accessory."""

    def __init__(self, hass, config):
        """Initialize the accessory."""
        self.hass = hass
        self.host = config[CONF_HOST]
        self.port = config[CONF_PORT]
        self.client = TCPClient(self.host, self.port)
        self.entities = {}

    async def connect(self):
        """Connect to the accessory."""
        await self.client.connect()
        # Fetch initial state and set up entities

    async def disconnect(self):
        """Disconnect from the accessory."""
        await self.client.disconnect()

    async def get_state(self, dp_id):
        """Get the state of an entity."""
        response = await self.client.send_command({"get": [{"dp_id": dp_id}]})
        return response["report"][0]["value"]

    async def set_state(self, dp_id, value):
        """Set the state of an entity."""
        await self.client.send_command({"set": [{"dp_id": dp_id, "value": value}]})
