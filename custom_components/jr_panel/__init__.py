"""The JR Touch Panel integration."""
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .jr_accessory import JRAccessory

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch", "fan", "light", "cover"]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the JR Touch Panel component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up JR Touch Panel from a config entry."""
    accessory = JRAccessory(hass, entry.data)

    try:
        await accessory.connect()
    except Exception as err:
        raise ConfigEntryNotReady from err

    hass.data[DOMAIN][entry.entry_id] = accessory

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    if unload_ok:
        accessory = hass.data[DOMAIN].pop(entry.entry_id)
        await accessory.disconnect()

    return unload_ok
