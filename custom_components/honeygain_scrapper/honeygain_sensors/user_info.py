from __future__ import annotations
from typing import Any, Callable, Dict, Optional

from ..const import DOMAIN
from ..coordinator import HoneyGainScrapperDataCoordinator
from ..helpers import sanitize_text, convert_objects
from .sensorClass import HoneyGainScrapperSensor

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_USERNAME, CONF_PASSWORD
from homeassistant.components.sensor import SensorEntity

class HoneyGainScrapperMeSensor(HoneyGainScrapperSensor):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)
        self._name = f'{config_entry.data[CONF_NAME]} Me'
        self._icon = "mdi:account"
        self._info_identifier = "user info"
    
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
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "me" in self._coordinator.data:
            return convert_objects(self._coordinator.data["me"])
        return {}

class HoneyGainScrapperNotificationsSensor(HoneyGainScrapperSensor):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)
        self._name = f'{config_entry.data[CONF_NAME]} notifications'
        self._icon = "mdi:message-badge"
        self._info_identifier = "user info"
    
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