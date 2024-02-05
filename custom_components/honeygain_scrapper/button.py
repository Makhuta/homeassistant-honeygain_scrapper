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
        self._available = True
        self._entity_name = entity_name
        self.attrs = {
                "success": False,
                "credits": 0,
            }

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
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    async def async_press(self) -> None:
        """Press the button."""
        try:
            data = await get_data(self._hass, f'{self.url}/{FUNCTIONS_OPEN_HONEYPOT}')
            self.attrs = data
            async_dispatcher_send(self._hass, BUTTON_EVENT, data)
        except:
            _LOGGER.exception("Error pressing Honeypot button on HoneyGain.")

    async def async_update(self):
        try:
            page_url = f'{self.url}/{INFOS_STATS}'
            data = await get_data(self._hass, page_url)
            today = date.today()
            today_string = today.strftime("%Y-%m-%d")

            out = {
                "success": False,
                "credits": 0,
            }

            if today_string in data:
                today_data = data[today_string]
                if "winnings" in today_data:
                    today_winnings = today_data["winnings"]
                    if "combined_of" in today_winnings:
                        today_combined_of = today_winnings["combined_of"]
                        if today_combined_of is not None and "lucky_pot" in today_combined_of:
                            today_lucky_pot = today_combined_of["lucky_pot"]
                            if today_lucky_pot is not None and "credits" in today_lucky_pot:
                                out = {
                                    "success": True,
                                    "credits": today_lucky_pot["credits"]
                                }

            self.attrs = out
        except:
            _LOGGER.exception("Error retrieving data from HoneyGain.")

"""
    async def async_reset_attributes(self) -> None:
        #Reset attrs.
        try:
            data = await get_data(self._hass, f'{self.url}/{FUNCTIONS_OPEN_HONEYPOT}')
            self.attrs = data
        except:
            _LOGGER.exception("Error reseting Honeypot button attributes on HoneyGain.")
"""