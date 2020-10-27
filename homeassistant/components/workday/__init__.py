"""The Workday integration."""
import asyncio

from datetime import datetime, timedelta
import logging
from typing import Any

import holidays
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorEntity
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


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Hello World component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Hello World from a config entry."""
    add_holidays = entry.data[CONF_ADD_HOLIDAYS]
    remove_holidays = entry.data[CONF_REMOVE_HOLIDAYS]
    country = entry.data[CONF_COUNTRY]
    days_offset = entry.data[CONF_OFFSET]
    excludes = entry.data[CONF_EXCLUDE]
    province = entry.data[CONF_PROVINCE]
    sensor_name = entry.data[CONF_NAME]
    workdays = entry.data[CONF_WORKDAYS]

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
