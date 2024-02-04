import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_PASSWORD, CONF_URL, CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_URL, DEFAULT_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required(CONF_URL, default=DEFAULT_URL): str
    }
)


class HoneyGainConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for the HoneyGain integration."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors = {}

        if user_input is not None:
            self._async_abort_entries_match({CONF_URL: user_input[CONF_URL]})
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
        
        return self.async_show_form(step_id="user", data_schema=USER_DATA_SCHEMA, errors=errors)