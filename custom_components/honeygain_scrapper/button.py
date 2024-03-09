from typing import Any, Callable, Dict, Optional

from homeassistant.components.button import ButtonEntity
from homeassistant.const import CONF_NAME, CONF_USERNAME
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.typing import (
    ConfigType,
    HomeAssistantType,
)

from .helpers import sanitize_text
from .const import (
    DOMAIN,
    BUTTON_EVENT,
)
from .coordinator import HoneyGainScrapperDataCoordinator

async def async_setup_entry(
    hass: HomeAssistantType,
    config_entry: ConfigType,
    async_add_entities: Callable,
) -> None:
    """Set up HoneyGain button from config entry."""
    coordinator: HoneyGainScrapperDataCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([HoneyGainScrapperOpenHoneyPot(coordinator, config_entry)], update_before_add=True)



class HoneyGainScrapperOpenHoneyPot(ButtonEntity):
    def __init__(self, coordinator: HoneyGainScrapperDataCoordinator, config_entry: ConfigType) -> None:
        """Initialize a open_honeypot button entity."""
        self._coordinator = coordinator
        self._name = f'{config_entry.data[CONF_NAME]} honeypot'
        self._entity_name = config_entry.data[CONF_NAME]
        self._username = config_entry.data[CONF_USERNAME]

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
        return f'{sanitize_text(self._name)}_{self._username}'
    
    @property
    def device_info(self):
        return {"name": f'{self._entity_name} functions' ,"manufacturer": "HoneyGain", "model": "Scrapper", "identifiers": {(DOMAIN, f'{self._username}{self._entity_name} functions')}}

    async def async_press(self) -> None:
        """Press the button."""
        if "honeypot" in self._coordinator.data:
            if self._coordinator.hass.async_add_executor_job(self._coordinator.client.openHoneyPot, self._coordinator.data["honeypot"]):
                async_dispatcher_send(self._coordinator.hass, BUTTON_EVENT)