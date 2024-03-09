from __future__ import annotations
from typing import Any, Callable, Dict, Optional

from ..const import DOMAIN, BUTTON_EVENT
from ..coordinator import HoneyGainScrapperDataCoordinator
from ..helpers import sanitize_text, convert_objects

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_ID
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect


class HoneyGainScrapperHoneyPotSensor(CoordinatorEntity[HoneyGainScrapperDataCoordinator], SensorEntity):
    """Representation of a HoneyGain sensor."""

    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = f'{config_entry.data[CONF_NAME]} honeypot'
        self._unit_of_measurement = "credits"
        self._entity_name = config_entry.data[CONF_NAME]
        self._username = config_entry.data[CONF_USERNAME]

        async_dispatcher_connect(coordinator.hass, BUTTON_EVENT.format(config_entry.entry_id), coordinator.async_refresh)

    
    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def icon(self):
        return "mdi:beehive-outline"

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
        if "honeypot" in self._coordinator.data:
            if "winning_credits" in self._coordinator.data["honeypot"]:
                return True
        return false #False need to fix
    
    @property
    def state(self) -> Optional[str]:
        if "honeypot" in self._coordinator.data:
            if "winning_credits" in self._coordinator.data["honeypot"]:
                return float(self._coordinator.data["honeypot"]["winning_credits"])
        return 0.0

    @property
    def device_info(self):
        return {"name": f'{self._entity_name} functions' ,"manufacturer": "HoneyGain", "model": "Scrapper", "identifiers": {(DOMAIN, f'{self._username}{self._entity_name} functions')}}
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        if "honeypot" in self._coordinator.data:
            if "progress_bytes" in self._coordinator.data["honeypot"] and "max_bytes" in self._coordinator.data["honeypot"] and "winning_credits" in self._coordinator.data["honeypot"]:
                return {
                    "success": self._coordinator.data["honeypot"]["winning_credits"] is not None,
                    "can_open": int(self._coordinator.data["honeypot"]["progress_bytes"]) == int(self._coordinator.data["honeypot"]["max_bytes"]),
                    "credits": float(self._coordinator.data["honeypot"]["winning_credits"])
                }
        return {
            "success": False,
            "can_open": False,
            "credits": 0.0
        }