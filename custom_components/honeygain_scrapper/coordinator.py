from __future__ import annotations

from datetime import timedelta
import logging
from typing import Dict, Any

from .hg_api import HG_Api, LoginBrokeDown

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.const import CONF_NAME

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class HoneyGainScrapperDataCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, client: HG_Api) -> None:
        self.client = client

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_method=self._async_update_data,
            update_interval=timedelta(minutes=10),
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        try:
            return await self.hass.async_add_executor_job(self.client.updateData)
        except LoginBrokeDown as exc:
            raise ConfigEntryError("HoneyGain Login broke (can be fixed by integration restart)") from exc
        except Exception as exc:
            raise ConfigEntryError("HoneyGain encoutered unknown") from exc
