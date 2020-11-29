"""Config flow for Workday integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions

from .const import DOMAIN  # pylint:disable=unused-import

from homeassistant.const import CONF_NAME, CONF_EXCLUDE, CONF_OFFSET, WEEKDAYS
from .const import (
    DEFAULT_WORKDAYS,
    DEFAULT_EXCLUDES,
    DEFAULT_NAME,
    DEFAULT_OFFSET,
)
from .binary_sensor import (
    CONF_COUNTRY,
    CONF_PROVINCE,
    CONF_WORKDAYS,
    CONF_ADD_HOLIDAYS,
    CONF_REMOVE_HOLIDAYS,
)

import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    # TODO validate the data can be used to set up a connection.

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    add_holidays = entry.data[CONF_ADD_HOLIDAYS]
    remove_holidays = entry.data[CONF_REMOVE_HOLIDAYS]
    country = entry.data[CONF_COUNTRY]
    days_offset = entry.data[CONF_OFFSET]
    excludes = entry.data[CONF_EXCLUDE]
    province = entry.data[CONF_PROVINCE]
    sensor_name = entry.data[CONF_NAME]
    workdays = entry.data[CONF_WORKDAYS]

    # Return info that you want to store in the config entry.
    return {"title": "Name of the device"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Workday."""

    VERSION = 1
    # TODO pick one of the available connection classes in homeassistant/config_entries.py
    CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                user_input[CONF_ADD_HOLIDAYS] = info["title"]
                user_input[CONF_REMOVE_HOLIDAYS] = info["title"]
                user_input[CONF_COUNTRY] = info["title"]
                user_input[CONF_OFFSET] = info["title"]
                user_input[CONF_EXCLUDE] = info["title"]
                user_input[CONF_PROVINCE] = info["title"]
                user_input[CONF_NAME] = info["title"]
                user_input[CONF_WORKDAYS] = info["title"]
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        ALLOWED_DAYS = WEEKDAYS + ["holiday"]
        DATA_SCHEMA = vol.Schema(
            {
                vol.Required(CONF_COUNTRY): str,
                vol.Optional(CONF_EXCLUDE, default=DEFAULT_EXCLUDES): str,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Optional(CONF_OFFSET, default=DEFAULT_OFFSET): vol.Coerce(int),
                vol.Optional(CONF_PROVINCE): cv.string,
                vol.Optional(CONF_WORKDAYS, default=DEFAULT_WORKDAYS): str,
                vol.Optional(CONF_ADD_HOLIDAYS): str,
                vol.Optional(CONF_REMOVE_HOLIDAYS): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
