from __future__ import annotations
from typing import Any, Callable, Dict, Optional

from ..const import DOMAIN
from ..coordinator import HoneyGainScrapperDataCoordinator
from ..helpers import sanitize_text, convert_objects

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_USERNAME, CONF_PASSWORD
from homeassistant.components.sensor import SensorEntity

class HoneyGainScrapperMeSensor(CoordinatorEntity[HoneyGainScrapperDataCoordinator], SensorEntity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = f'{config_entry.data[CONF_NAME]} Me'
        self._entity_name = config_entry.data[CONF_NAME]
        self._username = config_entry.data[CONF_USERNAME]
    
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
        return f'{sanitize_text(self._name)}_{self._username}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if "me" in self._coordinator.data:
            if "email" in self._coordinator.data["me"]:
                return True
        return False
    
    @property
    def state(self) -> Optional[str]:
        if "me" in self._coordinator.data:
            if "email" in self._coordinator.data["me"]:
                return self._coordinator.data["me"]["email"]
        return "Unknown"

    @property
    def device_info(self):
        return {"name": f'{self._entity_name} user info', "manufacturer": "HoneyGain", "model": "Scrapper", "identifiers": {(DOMAIN, f'{self._username}{self._entity_name} user info')}}
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "me" in self._coordinator.data:
            return self._coordinator.data["me"]
        return {}

class HoneyGainScrapperNotificationsSensor(CoordinatorEntity[HoneyGainScrapperDataCoordinator], SensorEntity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = f'{config_entry.data[CONF_NAME]} notifications'
        self._entity_name = config_entry.data[CONF_NAME]
        self._username = config_entry.data[CONF_USERNAME]
    
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
        return f'{sanitize_text(self._name)}_{self._username}'
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if "notifications" in self._coordinator.data:
            return True
        return False
    
    @property
    def state(self) -> Optional[str]:
        if "notifications" in self._coordinator.data:
            return len(self._coordinator.data["notifications"])
        return 0

    @property
    def device_info(self):
        return {"name": f'{self._entity_name} user info' ,"manufacturer": "HoneyGain", "model": "Scrapper", "identifiers": {(DOMAIN, f'{self._username}{self._entity_name} user info')}}