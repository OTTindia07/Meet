"""TCP client for JR Panel."""
import asyncio
import json
from typing import Any, Dict

class JRPanelTCPClient:
    """TCP client for communicating with JR Panel."""

    def __init__(self, host: str, port: int = 4096):
        """Initialize the client."""
        self.host = host
        self._port = port
        self._reader = None
        self._writer = None

    async def _ensure_connected(self):
        """Ensure connection to the JR Panel."""
        if self._writer is None or self._writer.is_closing():
            self._reader, self._writer = await asyncio.open_connection(self.host, self._port)

    async def _send_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Send a command to the JR Panel and return the response."""
        await self._ensure_connected()
        json_command = json.dumps(command) + "\r\n"
        self._writer.write(json_command.encode())
        await self._writer.drain()

        response = await self._reader.readline()
        return json.loads(response.decode())

    async def get_switch_state(self, switch_id: int) -> bool:
        """Get the state of a switch."""
        command = {"get": [{"dp_id": 107 + switch_id}]}
        response = await self._send_command(command)
        return response["report"][0]["value"]

    async def set_switch(self, switch_id: int, state: bool):
        """Set the state of a switch."""
        command = {
            "set": [{
                "dp_id": 107 + switch_id,
                "identifier": f"switch_{switch_id}",
                "value": state
            }]
        }
        await self._send_command(command)

    async def get_fan_speed(self, fan_id: int) -> int:
        """Get the speed of a fan."""
        command = {"get": [{"dp_id": 117 + fan_id}]}
        response = await self._send_command(command)
        return response["report"][0]["value"]

    async def set_fan(self, fan_id: int, speed: int):
        """Set the speed of a fan."""
        command = {
            "set": [{
                "dp_id": 117 + fan_id,
                "identifier": f"fan_{fan_id}",
                "value": speed
            }]
        }
        await self._send_command(command)
