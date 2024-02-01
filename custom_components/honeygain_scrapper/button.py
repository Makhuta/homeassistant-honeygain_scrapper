from typing import Any, Callable, Dict, Optional
import re
import unicodedata
import logging

from homeassistant.helpers.entity import Entity

from homeassistant.helpers.typing import (
    ConfigType,
    HomeAssistantType,
)

from homeassistant.const import CONF_URL

from requests import get

from .const import (
    FUNCTIONS_OPEN_HONEYPOT
)

_LOGGER = logging.getLogger(__name__)

def sanitize_text(input_text):
    lowercase_text = str(input_text).lower()
    normalized_text = ''.join(c for c in unicodedata.normalize('NFD', lowercase_text) if unicodedata.category(c) != 'Mn')
    sanitized_text = re.sub(r'[^a-zA-Z0-9_]', '_', normalized_text)

    return sanitized_text

async def get_data(hass: HomeAssistantType, url: CONF_URL):
    try:
        res = await hass.async_add_executor_job(get, url)

        if res.status_code != 200:
            if res.status_code == 404:
                _LOGGER.exception(f'Unable to connect to URL: {url}')
            else:
                _LOGGER.exception(f'There was some unexpected error. Status code: {res.status_code}')
        else:
            return res.json()
    except:
        _LOGGER.exception("Error retrieving data from HoneyGain.")
    return {"success":False,"credits":0}

async def async_setup_entry(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
) -> None:
    """Set up Plex button from config entry."""
    async_add_entities([HoneyGainScrapperOpenHoneyPot(hass, config[CONF_URL])])

class HoneyGainScrapperOpenHoneyPot(Entity):
    def __init__(self, hass: HomeAssistantType, url: CONF_URL) -> None:
        """Initialize a open_honeypot button entity."""
        self.url = url
        self._hass = hass
        self._name = "HoneyGain open honeypot"
        self._available = True

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name
    
    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f'{sanitize_text(self._name)}_{self.url}'

    async def async_press(self) -> None:
        """Press the button."""
        try:
            data = await get_data(self._hass, f'{self.url}/{FUNCTIONS_OPEN_HONEYPOT}')
        except:
            _LOGGER.exception("Error pressing Honeypot button on HoneyGain.")