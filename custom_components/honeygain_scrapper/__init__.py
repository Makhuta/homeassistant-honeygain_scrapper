import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.dispatcher import async_dispatcher_connect


from homeassistant.const import (
    Platform,
)

from .const import DOMAIN, BUTTON_EVENT

PLATFORMS = [
    Platform.SENSOR,
    Platform.BUTTON
]

_LOGGER = logging.getLogger(__name__)


def handle_event(data):
    try:
        if "success" in data and "credits" in data:
            print(f'Honeypot was {"" if data["success"] == True else "not "} opened succesfully containing {data["credits"]} credits')
    except:
        _LOGGER.exception("Error printing data from Honeypot handler.")

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the HoneyGain Scrapper component."""
    # @TODO: Add setup code.
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = config_entry.data

    async_dispatcher_connect(hass, BUTTON_EVENT.format(config_entry.entry_id), handle_event)

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload HoneyGain config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )
    return unload_ok