from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
import logging
from typing import Any, Callable, Dict, Optional

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_USERNAME
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
    StateType,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HoneyGainScrapperDataCoordinator
from .honeygain_sensors import (
    devices,
    functions,
    stats,
    user_info
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistantType,
    config_entry: ConfigType,
    async_add_entities: Callable,
) -> None:
    coordinator: HoneyGainScrapperDataCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors_normal = [
        user_info.HoneyGainScrapperMeSensor(coordinator, config_entry),
        stats.HoneyGainScrapperStatsTodaySensor(coordinator, config_entry),
        stats.HoneyGainScrapperStatsTodayJTSensor(coordinator, config_entry),
        user_info.HoneyGainScrapperNotificationsSensor(coordinator, config_entry),
        stats.HoneyGainScrapperBalancesSensor(coordinator, config_entry),
        functions.HoneyGainScrapperHoneyPotSensor(coordinator, config_entry)
    ]

    if "stats" in coordinator.data:
        statsSensors = [
            stats.HoneyGainScrapperStatsSensor(coordinator, config_entry, s)
            for s in range(30)
        ]
    else:
        statsSensors = []

    if "devices" in coordinator.data:
        devicesList = [
            devices.HoneyGainScrapperDevicesSensor(coordinator, config_entry, d, coordinator.data["devices"][d]["id"])
            for d in range(len(coordinator.data["devices"]) if "devices" in coordinator.data else 0) if "id" in coordinator.data["devices"][d]
        ]
    else:
        devicesList = []

    sensors = sensors_normal + statsSensors + devicesList
    async_add_entities(sensors, update_before_add=True)