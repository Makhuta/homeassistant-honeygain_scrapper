from __future__ import annotations
from typing import Any, Callable, Dict, Optional

from ..const import DOMAIN
from ..coordinator import HoneyGainScrapperDataCoordinator
from ..helpers import sanitize_text, convert_objects
from .sensorClass import HoneyGainScrapperSensor

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_ID

class HoneyGainScrapperDevicesSensor(HoneyGainScrapperSensor):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry, id: CONF_ID, device_name: CONF_NAME):
        super().__init__(coordinator, config_entry)
        self._name = f'{config_entry.data[CONF_NAME]} Device {device_name}'
        self._id = id
        self._icon = "mdi:devices"
        self._info_identifier = "devices"
    
    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if "devices" in self._coordinator.data:
            if self._id < len(self._coordinator.data["devices"]):
                if "id" in self._coordinator.data["devices"][self._id]:
                    return True
        return False
    
    @property
    def state(self) -> Optional[str]:
        if "devices" in self._coordinator.data:
            if self._id < len(self._coordinator.data["devices"]):
                if "id" in self._coordinator.data["devices"][self._id]:
                    return self._coordinator.data["devices"][self._id]["id"]
        return "Unknown"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "devices" in self._coordinator.data:
            if self._id < len(self._coordinator.data["devices"]):
                return convert_objects(self._coordinator.data["devices"][self._id])
        return {}