from __future__ import annotations
import logging
from typing import Any

from .hg_api import FailedToLogin
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_NAME, CONF_USERNAME, CONF_PASSWORD

from .const import DEFAULT_NAME, DEFAULT_USERNAME, DEFAULT_PASSWORD, DOMAIN
from .helpers import setup_client

_LOGGER = logging.getLogger(__name__)

USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str
    }
)

class HoneyGainConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for the HoneyGain integration."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ):
        errors = {}

        if user_input is not None:
            self._async_abort_entries_match({CONF_USERNAME: user_input[CONF_USERNAME]})
            try:
                await self.hass.async_add_executor_job(
                    setup_client,
                    self.hass,
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD]
                )
            except FailedToLogin:
                errors = {"base": "failed_to_login"}
            else:
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        schema = self.add_suggested_values_to_schema(USER_DATA_SCHEMA, user_input)
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)