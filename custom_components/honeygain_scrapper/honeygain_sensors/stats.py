from __future__ import annotations
from typing import Any, Callable, Dict, Optional

from ..const import DOMAIN
from ..coordinator import HoneyGainScrapperDataCoordinator
from ..helpers import sanitize_text, convert_objects, containsAllSubstr, sumAll
from .sensorClass import HoneyGainScrapperSensor

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_ID
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.typing import StateType

class HoneyGainScrapperStatsSensor(HoneyGainScrapperSensor):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry, id: CONF_ID):
        super().__init__(coordinator, config_entry)
        self._name = f'{config_entry.data[CONF_NAME]} stats past {"0" if (30 - (id + 1)) < 10 else ""}{30 - (id + 1)}'
        self._unit_of_measurement = "credits"
        self._id = id
        self._icon = "mdi:history"
        self._info_identifier = "month stats"
        self._categories = [
                    "gathering",
                    "content_delivery",
                    "referrals",
                    "winnings",
                    "other"
                ]

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if "stats" in self._coordinator.data:
            if self._id < len(self._coordinator.data["stats"]):
                return containsAllSubstr(self._categories, self._coordinator.data["stats"][self._id], "credits")
        return False
    
    @property
    def state(self) -> Optional[str]:
        if "stats" in self._coordinator.data:
            if self._id < len(self._coordinator.data["stats"]):
                return sumAll(self._categories, self._coordinator.data["stats"][self._id])
        return 0.0

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "stats" in self._coordinator.data:
            if self._id < len(self._coordinator.data["stats"]):
                return convert_objects(self._coordinator.data["stats"][self._id])
        return {}

class HoneyGainScrapperStatsTodaySensor(HoneyGainScrapperSensor):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)
        self._name = f'{config_entry.data[CONF_NAME]} stats today'
        self._unit_of_measurement = "credits"
        self._icon = "mdi:calendar-today"
        self._info_identifier = "stats"

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if "stats_today" in self._coordinator.data:
            if "total_credits" in self._coordinator.data["stats_today"]:
                return True
        return False
    
    @property
    def state(self) -> Optional[str]:
        """Return the value of the sensor."""
        if "stats_today" in self._coordinator.data:
            if "total_credits" in self._coordinator.data["stats_today"]:
                return self._coordinator.data["stats_today"]["total_credits"]
        return 0.0

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "stats_today" in self._coordinator.data:
            return convert_objects(self._coordinator.data["stats_today"])
        return {}

class HoneyGainScrapperStatsTodayJTSensor(HoneyGainScrapperSensor):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)
        self._name = f'{config_entry.data[CONF_NAME]} stats today JT'
        self._unit_of_measurement = "credits"
        self._icon = "mdi:calendar-today-outline"
        self._info_identifier = "stats"

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if "stats_today_jt" in self._coordinator.data:
            if "total_credits" in self._coordinator.data["stats_today_jt"]:
                return True
        return False
    
    @property
    def state(self) -> Optional[str]:
        if "stats_today_jt" in self._coordinator.data:
            if "total_credits" in self._coordinator.data["stats_today_jt"]:
                return self._coordinator.data["stats_today_jt"]["total_credits"]
        return 0.0

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "stats_today_jt" in self._coordinator.data:
            return convert_objects(self._coordinator.data["stats_today_jt"])

        return {}

class HoneyGainScrapperBalancesSensor(HoneyGainScrapperSensor):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)
        self._name = f'{config_entry.data[CONF_NAME]} balances'
        self._unit_of_measurement = "credits"
        self._icon = "mdi:sack"
        self._info_identifier = "stats"
    
    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement
    
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
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "balances" in self._coordinator.data:
            return convert_objects(self._coordinator.data["balances"])
        return {}