from typing import Any, Callable, Dict, Optional
import re
import unicodedata
import logging
from datetime import date

from homeassistant.helpers.entity import Entity
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.dispatcher import async_dispatcher_send

from homeassistant.helpers.typing import (
    ConfigType,
    HomeAssistantType,
)

from homeassistant.const import CONF_URL, CONF_NAME

from requests import get

from .const import (
    DOMAIN,
    BUTTON_EVENT,
    FUNCTIONS_OPEN_HONEYPOT,
    INFOS_STATS,
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
    config_entry: ConfigType,
    async_add_entities: Callable,
) -> None:
    """Set up Plex button from config entry."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([HoneyGainScrapperOpenHoneyPot(hass, config[CONF_URL], config[CONF_NAME])], update_before_add=True)

class HoneyGainScrapperOpenHoneyPot(ButtonEntity):
    def __init__(self, hass: HomeAssistantType, url: CONF_URL, entity_name: CONF_NAME) -> None:
        """Initialize a open_honeypot button entity."""
        self.url = url
        self._hass = hass
        self._name = "HoneyGain open honeypot"
        self._entity_name = entity_name

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def icon(self):
        return "mdi:beehive-outline"
    
    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f'{sanitize_text(self._name)}_{self.url}'
    
    @property
    def device_info(self):
        return {"name": f'{self._entity_name} functions' ,"manufacturer": "HoneyGain", "model": "Scrapper", "identifiers": {(DOMAIN, f'{self.url}{self._entity_name} functions')}}

    async def async_press(self) -> None:
        """Press the button."""
        try:
            await get_data(self._hass, f'{self.url}/{FUNCTIONS_OPEN_HONEYPOT}')
            async_dispatcher_send(self._hass, BUTTON_EVENT)
        except:
            _LOGGER.exception("Error pressing Honeypot button on HoneyGain.")