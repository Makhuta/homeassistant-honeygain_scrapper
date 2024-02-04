from typing import Any, Callable, Dict, Optional
import logging
from datetime import timedelta
import re
import unicodedata

from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import CONF_URL, CONF_NAME, CONF_ID

from requests import get

from .const import (
    INFOS_ME,
    INFOS_DEVICES,
    INFOS_STATS,
    INFOS_STATS_TODAY,
    INFOS_STATS_TODAY_JT,
    INFOS_NOTIFICATIONS,
    INFOS_PAYOUTS,
    INFOS_BALANCES
)

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=10)

def convert_objects(object: Dict[str, Any]) -> Dict[str, Any]:
    data = {}
    for key in object:
        item = object[key]
        if type(item) == dict:
            data[key] = [convert_objects(item)]
        else:
            data[key] = item

    return data

def sanitize_text(input_text):
    lowercase_text = str(input_text).lower()
    normalized_text = ''.join(c for c in unicodedata.normalize('NFD', lowercase_text) if unicodedata.category(c) != 'Mn')
    sanitized_text = re.sub(r'[^a-zA-Z0-9_]', '_', normalized_text)

    return sanitized_text

async def get_devices(hass: HomeAssistantType, url: CONF_URL):
    page_url = f'{url}/{INFOS_DEVICES}'
    return await get_data(hass, page_url)

async def get_stats(hass: HomeAssistantType, url: CONF_URL):
    page_url = f'{url}/{INFOS_STATS}'
    data = await get_data(hass, page_url)
    stats = []
    last_update = ""
    if "last_updated" in data:
        last_update = data["last_updated"]
    for key in data:
        if type(data[key]) == dict:
            data[key]["date"] = key
            data[key]["last_updated"] = last_update
            stats.append(data[key])
    return stats


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
    return {}

def filter_array(id: CONF_ID, arr):
    for item in arr:
        if item["id"] == id:
            return item

    return {}

async def async_setup_entry(
    hass: HomeAssistantType,
    config_entry: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    config = config_entry.data
    sensors_normal = [
        HoneyGainScrapperMeSensor(hass, config[CONF_URL], config[CONF_NAME]),
        HoneyGainScrapperStatsTodaySensor(hass, config[CONF_URL], config[CONF_NAME]),
        HoneyGainScrapperStatsTodayJTSensor(hass, config[CONF_URL], config[CONF_NAME]),
        HoneyGainScrapperNotificationsSensor(hass, config[CONF_URL], config[CONF_NAME]),
        HoneyGainScrapperBalancesSensor(hass, config[CONF_URL], config[CONF_NAME])
    ]

    try:
        devices = [
            HoneyGainScrapperDevicesSensor(
                hass, 
                config[CONF_URL], 
                sanitize_text(d["title"] if d["title"] != None else d["model"]), 
                d["id"],
                config[CONF_NAME]) 
                for d in await get_devices(hass, config[CONF_URL]
            )
        ]
    except:
        _LOGGER.exception("Error retrieving devices from HoneyGain.")
        devices = []

    try:
        stats = await get_stats(hass, config[CONF_URL])

        statsSensors = [HoneyGainScrapperStatsSensor(hass, config[CONF_URL], s, config[CONF_NAME]) for s in range(len(stats))]
    except:
        _LOGGER.exception("Error retrieving devices from HoneyGain.")
        statsSensors = []

    sensors = sensors_normal + devices + statsSensors
    async_add_entities(sensors, update_before_add=True)

class HoneyGainScrapperMeSensor(Entity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, hass: HomeAssistantType, url: CONF_URL, entity_name: CONF_NAME):
        self.url = url
        self._hass = hass
        self._name = f'{entity_name} Me'
        self._state = ""
        self._available = True
        self.attrs: Dict[str, Any] = {}
    
    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def icon(self):
        return "mdi:account"
    
    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f'{sanitize_text(self._name)}_{self.url}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available
    
    @property
    def state(self) -> Optional[str]:
        return self._state
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs
    
    async def async_update(self):
        try:
            page_url = f'{self.url}/{INFOS_ME}'
            data = await get_data(self._hass, page_url)

            self._state = data["email"]
            self.attrs = convert_objects(data)

            self._available = True
        except:
            self._available = False
            _LOGGER.exception("Error retrieving data from HoneyGain.")

class HoneyGainScrapperDevicesSensor(Entity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, hass: HomeAssistantType, url: CONF_URL, name: CONF_NAME, id: CONF_ID, entity_name: CONF_NAME):
        self.url = url
        self._hass = hass
        self._name = f'{entity_name} Device {name}'
        self._state = ""
        self._available = True
        self._id = id
        self.attrs: Dict[str, Any] = {}
    
    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def icon(self):
        return "mdi:devices"
    
    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f'{sanitize_text(self._name)}_{self.url}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available
    
    @property
    def state(self) -> Optional[str]:
        return self._state
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs
    
    async def async_update(self):
        try:
            page_url = f'{self.url}/{INFOS_DEVICES}'
            data = filter_array(self._id, await get_data(self._hass, page_url))

            if "id" in data:
                self._state = data["id"]
            self.attrs = convert_objects(data)

            self._available = True
        except:
            self._available = False
            _LOGGER.exception("Error retrieving data from HoneyGain.")

class HoneyGainScrapperStatsSensor(Entity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, hass: HomeAssistantType, url: CONF_URL, id: CONF_ID, entity_name: CONF_NAME):
        self.url = url
        self._hass = hass
        self._name = f'{entity_name} stats past {"0" if (30 - (id + 1)) < 10 else ""}{30 - (id + 1)}'
        self._unit_of_measurement = "credits"
        self._id = id
        self._state = ""
        self._available = True
        self.attrs: Dict[str, Any] = {}
    
    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def icon(self):
        return "mdi:history"

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement
    
    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f'{sanitize_text(self._name)}_{self.url}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available
    
    @property
    def state(self) -> Optional[str]:
        return self._state
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs
    
    async def async_update(self):
        try:
            data = await get_stats(self._hass, self.url)

            if len(data) > self._id:
                if "gathering" in data[self._id] and "credits" in data[self._id]["gathering"]:
                    self._state = data[self._id]["gathering"]["credits"]
                else:
                    self._state = -1
                self.attrs = convert_objects(data[self._id])

                self._available = True
            else:
                self._available = False

        except:
            self._available = False
            _LOGGER.exception("Error retrieving stats from HoneyGain.")

class HoneyGainScrapperStatsTodaySensor(Entity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, hass: HomeAssistantType, url: CONF_URL, entity_name: CONF_NAME):
        self.url = url
        self._hass = hass
        self._name = f'{entity_name} stats today'
        self._unit_of_measurement = "credits"
        self._state = ""
        self._available = True
        self.attrs: Dict[str, Any] = {}
    
    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def icon(self):
        return "mdi:calendar-today"

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement
    
    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f'{sanitize_text(self._name)}_{self.url}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available
    
    @property
    def state(self) -> Optional[str]:
        return self._state
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs
    
    async def async_update(self):
        try:
            page_url = f'{self.url}/{INFOS_STATS_TODAY}'
            data = await get_data(self._hass, page_url)

            if "total" in data:
                del data["total"]
            if "winning" in data:
                del data["winning"]
            if "referral" in data:
                del data["referral"]
            if "other" in data:
                del data["other"]
            if "cdn" in data:
                data["cdn_credits"] = data["cdn"]["credits"]
                data["cdn_seconds"] = data["cdn"]["seconds"]
                del data["cdn"]
            if "gathering" in data:
                data["gathering_credits"] = data["gathering"]["credits"]
                del data["gathering"]

            self._state = data["total_credits"]
            self.attrs = convert_objects(data)

            self._available = True
        except:
            self._available = False
            _LOGGER.exception("Error retrieving today stats from HoneyGain.")

class HoneyGainScrapperStatsTodayJTSensor(Entity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, hass: HomeAssistantType, url: CONF_URL, entity_name: CONF_NAME):
        self.url = url
        self._hass = hass
        self._name = f'{entity_name} stats today JT'
        self._unit_of_measurement = "credits"
        self._state = ""
        self._available = True
        self.attrs: Dict[str, Any] = {}
    
    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def icon(self):
        return "mdi:calendar-today-outline"

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement
    
    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f'{sanitize_text(self._name)}_{self.url}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available
    
    @property
    def state(self) -> Optional[str]:
        return self._state
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs
    
    async def async_update(self):
        try:
            page_url = f'{self.url}/{INFOS_STATS_TODAY_JT}'
            data = await get_data(self._hass, page_url)

            if "total" in data:
                data["total_credits"] = data["total"]["credits"]
                del data["total"]
            if "winning" in data:
                data["winning_credits"] = data["winning"]["credits"]
                del data["winning"]
            if "referral" in data:
                data["referral_credits"] = data["referral"]["credits"]
                del data["referral"]
            if "other" in data:
                data["other_credits"] = data["other"]["credits"]
                del data["other"]
            if "bonus" in data:
                data["bonus_credits"] = data["bonus"]["credits"]
                del data["bonus"]
            if "cdn" in data:
                data["cdn_credits"] = data["cdn"]["credits"]
                data["cdn_seconds"] = data["cdn"]["seconds"]
                del data["cdn"]
            if "gathering" in data:
                data["gathering_credits"] = data["gathering"]["credits"]
                data["gathering_bytes"] = data["gathering"]["bytes"]
                del data["gathering"]
            

            self._state = data["total_credits"]
            self.attrs = convert_objects(data)

            self._available = True
        except:
            self._available = False
            _LOGGER.exception("Error retrieving today stats from HoneyGain.")

class HoneyGainScrapperNotificationsSensor(Entity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, hass: HomeAssistantType, url: CONF_URL, entity_name: CONF_NAME):
        self.url = url
        self._hass = hass
        self._name = f'{entity_name} notifications'
        self._state = ""
        self._available = True
    
    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def icon(self):
        return "mdi:message-badge"
    
    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f'{sanitize_text(self._name)}_{self.url}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available
    
    @property
    def state(self) -> Optional[str]:
        return self._state
    
    async def async_update(self):
        try:
            page_url = f'{self.url}/{INFOS_NOTIFICATIONS}'
            data = await get_data(self._hass, page_url)

            self._state = len(data)

            self._available = True
        except:
            self._available = False
            _LOGGER.exception("Error retrieving nitifications from HoneyGain.")

class HoneyGainScrapperBalancesSensor(Entity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, hass: HomeAssistantType, url: CONF_URL, entity_name: CONF_NAME):
        self.url = url
        self._hass = hass
        self._name = f'{entity_name} balances'
        self._unit_of_measurement = "credits"
        self._state = ""
        self._available = True
        self.attrs: Dict[str, Any] = {}
    
    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def icon(self):
        return "mdi:sack"

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement
    
    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f'{sanitize_text(self._name)}_{self.url}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available
    
    @property
    def state(self) -> Optional[str]:
        return self._state
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        return self.attrs
    
    async def async_update(self):
        try:
            page_url = f'{self.url}/{INFOS_BALANCES}'
            data = await get_data(self._hass, page_url)

            if "payout" in data:
                self._state = data["payout"]["credits"]
            else:
                self._state = -1

            self.attrs = convert_objects(data)

            self._available = True
        except:
            self._available = False
            _LOGGER.exception("Error retrieving today stats from HoneyGain.")




