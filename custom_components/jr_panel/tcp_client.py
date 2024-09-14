
"""TCP client for JR Touch Panel."""
import asyncio
import json
import logging

_LOGGER = logging.getLogger(__name__)

class TCPClient:
    """TCP client for JR Touch Panel."""

    def __init__(self, host, port):
        """Initialize the TCP client."""
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        """Connect to the TCP server."""
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    async def disconnect(self):
        """Disconnect from the TCP server."""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

    async def send_command(self, command):
        """Send a command to the TCP server."""
        if not self.writer:
            await self.connect()
        self.writer.write(json.dumps(command).encode() + b'\r\n')
        await self.writer.drain()
        response = await self.reader.readline()
        return json.loads(response.decode())
