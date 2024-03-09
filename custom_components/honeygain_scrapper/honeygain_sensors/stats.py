from __future__ import annotations
from typing import Any, Callable, Dict, Optional

from ..const import DOMAIN
from ..coordinator import HoneyGainScrapperDataCoordinator
from ..helpers import sanitize_text, convert_objects

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_ID
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.typing import StateType

class HoneyGainScrapperStatsSensor(CoordinatorEntity[HoneyGainScrapperDataCoordinator], SensorEntity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry, id: CONF_ID):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = f'{config_entry.data[CONF_NAME]} stats past {"0" if (30 - (id + 1)) < 10 else ""}{30 - (id + 1)}'
        self._unit_of_measurement = "credits"
        self._id = id
        self._entity_name = config_entry.data[CONF_NAME]
        self._username = config_entry.data[CONF_USERNAME]
    
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
        return f'{sanitize_text(self._name)}_{self._username}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if "stats" in self._coordinator.data:
            if self._id < len(self._coordinator.data["stats"]):
                if "gathering" in self._coordinator.data["stats"][self._id] and "credits" in self._coordinator.data["stats"][self._id]["gathering"]:
                    return True
        return False
    
    @property
    def state(self) -> Optional[str]:
        if "stats" in self._coordinator.data:
            if self._id < len(self._coordinator.data["stats"]):
                if "gathering" in self._coordinator.data["stats"][self._id] and "credits" in self._coordinator.data["stats"][self._id]["gathering"]:
                    return self._coordinator.data["stats"][self._id]["gathering"]["credits"]
        return 0.0

    @property
    def device_info(self):
        return {"name": f'{self._entity_name} month stats' ,"manufacturer": "HoneyGain", "model": "Scrapper", "identifiers": {(DOMAIN, f'{self._username}{self._entity_name} month stats')}}
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "stats" in self._coordinator.data:
            if self._id < len(self._coordinator.data["stats"]):
                return self._coordinator.data["stats"][self._id]
        return {}

class HoneyGainScrapperStatsTodaySensor(CoordinatorEntity[HoneyGainScrapperDataCoordinator], SensorEntity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = f'{config_entry.data[CONF_NAME]} stats today'
        self._unit_of_measurement = "credits"
        self._entity_name = config_entry.data[CONF_NAME]
        self._username = config_entry.data[CONF_USERNAME]
    
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
        return f'{sanitize_text(self._name)}_{self._username}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if "stats_today" in self._coordinator.data:
            if "gathering_credits" in self._coordinator.data["stats_today"]:
                return True
        return False
    
    @property
    def state(self) -> Optional[str]:
        """Return the value of the sensor."""
        if "stats_today" in self._coordinator.data:
            if "gathering_credits" in self._coordinator.data["stats_today"]:
                return self._coordinator.data["stats_today"]["gathering_credits"]
        return 0.0

    @property
    def device_info(self):
        return {"name": f'{self._entity_name} stats' ,"manufacturer": "HoneyGain", "model": "Scrapper", "identifiers": {(DOMAIN, f'{self._username}{self._entity_name} stats')}}
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "stats_today" in self._coordinator.data:
            return convert_objects(self._coordinator.data["stats_today"])
        return {}

class HoneyGainScrapperStatsTodayJTSensor(CoordinatorEntity[HoneyGainScrapperDataCoordinator], SensorEntity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = f'{config_entry.data[CONF_NAME]} stats today JT'
        self._unit_of_measurement = "credits"
        self._entity_name = config_entry.data[CONF_NAME]
        self._username = config_entry.data[CONF_USERNAME]

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
        return f'{sanitize_text(self._name)}_{self._username}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if "stats_today_jt" in self._coordinator.data:
            if "gathering_credits" in self._coordinator.data["stats_today_jt"]:
                return True
        return False
    
    @property
    def state(self) -> Optional[str]:
        if "stats_today_jt" in self._coordinator.data:
            if "gathering_credits" in self._coordinator.data["stats_today_jt"]:
                return self._coordinator.data["stats_today_jt"]["gathering_credits"]
        return 0.0

    @property
    def device_info(self):
        return {"name": f'{self._entity_name} stats' ,"manufacturer": "HoneyGain", "model": "Scrapper", "identifiers": {(DOMAIN, f'{self._username}{self._entity_name} stats')}}
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "stats_today_jt" in self._coordinator.data:
            return convert_objects(self._coordinator.data["stats_today_jt"])

        return {}

class HoneyGainScrapperBalancesSensor(CoordinatorEntity[HoneyGainScrapperDataCoordinator], SensorEntity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = f'{config_entry.data[CONF_NAME]} balances'
        self._unit_of_measurement = "credits"
        self._entity_name = config_entry.data[CONF_NAME]
        self._username = config_entry.data[CONF_USERNAME]
    
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
        return f'{sanitize_text(self._name)}_{self._username}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if "balances" in self._coordinator.data:
            if "payout" in self._coordinator.data["balances"] and "credits" in self._coordinator.data["balances"]["payout"]:
                return True
        return False
    
    @property
    def state(self) -> Optional[str]:
        if "balances" in self._coordinator.data:
            if "payout" in self._coordinator.data["balances"] and "credits" in self._coordinator.data["balances"]["payout"]:
                return self._coordinator.data["balances"]["payout"]["credits"]
        return 0.0

    @property
    def device_info(self):
        return {"name": f'{self._entity_name} stats' ,"manufacturer": "HoneyGain", "model": "Scrapper", "identifiers": {(DOMAIN, f'{self._username}{self._entity_name} stats')}}
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "balances" in self._coordinator.data:
            return convert_objects(self._coordinator.data["balances"])
        return {}