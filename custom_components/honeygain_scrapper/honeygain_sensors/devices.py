from __future__ import annotations
from typing import Any, Callable, Dict, Optional

from ..const import DOMAIN
from ..coordinator import HoneyGainScrapperDataCoordinator
from ..helpers import sanitize_text, convert_objects

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_ID
from homeassistant.components.sensor import SensorEntity

class HoneyGainScrapperDevicesSensor(CoordinatorEntity[HoneyGainScrapperDataCoordinator], SensorEntity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry, id: CONF_ID, device_name: CONF_NAME):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = f'{config_entry.data[CONF_NAME]} Device {device_name}'
        self._id = id
        self._entity_name = config_entry.data[CONF_NAME]
        self._username = config_entry.data[CONF_USERNAME]
    
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
        return f'{sanitize_text(self._name)}_{self._username}'
    
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
    def device_info(self):
        return {"name": f'{self._entity_name} devices' ,"manufacturer": "HoneyGain", "model": "Scrapper", "identifiers": {(DOMAIN, f'{self._username}{self._entity_name} devices')}}
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "devices" in self._coordinator.data:
            if self._id < len(self._coordinator.data["devices"]):
                return self._coordinator.data["devices"][self._id]
        return {}