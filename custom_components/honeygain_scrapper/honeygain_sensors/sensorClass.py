from ..coordinator import HoneyGainScrapperDataCoordinator
from ..helpers import sanitize_text, convert_objects
from ..const import DOMAIN

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_USERNAME

class HoneyGainScrapperSensor(CoordinatorEntity[HoneyGainScrapperDataCoordinator], SensorEntity):
    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._entity_name = config_entry.data[CONF_NAME]
        self._username = config_entry.data[CONF_USERNAME]
    
    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f'{sanitize_text(self._name)}_{self._username}'

    @property
    def device_info(self):
        return {
            "name": f'{self._entity_name} {self._info_identifier}',
            "manufacturer": "HoneyGain", 
            "model": "Scrapper", 
            "identifiers": {(DOMAIN, f'{self._username}{self._entity_name} {self._info_identifier}')}
            }
    