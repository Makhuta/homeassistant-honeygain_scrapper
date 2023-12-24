from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import CURRENCY_DOLLAR
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity import generate_entity_id
from datetime import timedelta
from pyHoneygain import HoneyGain
import json
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
import voluptuous as vol
import logging

CONF_USERNAME = 'username'
CONF_PASSWORD = 'password'

SCAN_INTERVAL = timedelta(minutes=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

_LOGGER = logging.getLogger(__name__)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    hg_user = HoneyGain()
    try:
        hg_user.login(config.get(CONF_USERNAME), config.get(CONF_PASSWORD))
        add_entities([UserSensor(hg_user), MonthSensor(hg_user), TodaySensor(hg_user), BalanceSensor(hg_user)], True)
    except:
        _LOGGER.error("Error while getting logging in")


class UserSensor(SensorEntity):
    def __init__(self, hg_user):
        self._state = None
        self._user_data = {}
        self._hg_user = hg_user

    @property
    def name(self):
        return 'HoneyGain User'

    @property
    def unique_id(self):
        return f"honeygain_user_stats"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._user_data
    
    def update(self):
        try:
            myData = self._hg_user.me()

            self._user_data = {
                "id": myData["id"],
                "email": myData["email"],
                "email_confirmed": myData["email_confirmed"],
                "status": myData["status"],
                "total_devices": myData["total_devices"],
                "referral_code": myData["referral_code"],
                "created_at": myData["created_at"],
                "active_devices": myData["active_devices_count"],
                "jt_toggle": myData["jt_toggle"]
            }
            self._state = myData["email"]
        except:
            _LOGGER.error("Error while getting user data")
    

class TodaySensor(SensorEntity):
    def __init__(self, hg_user):
        self._state = None
        self._today_stats = {}
        self._hg_user = hg_user

    @property
    def name(self):
        return 'HoneyGain Today'

    @property
    def unique_id(self):
        return f"honeygain_today_stats"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._today_stats
    
    def update(self):
        try:
            statsToday = self._hg_user.stats_today()
            self._today_stats = {
                "gather credit": [
                    statsToday["gathering"]["credits"]
                ],
                "gather bytes": [
                    statsToday["gathering"]["bytes"]
                ],
                "referals": statsToday["referral"]["credits"],
                "winnings": statsToday["winning"]["credits"],
                "other": statsToday["other"]["credits"]
            }
            self._state = float(statsToday["gathering"]["credits"]) + float(statsToday["winning"]["credits"])
        except:
            _LOGGER.error("Error while getting today data")


class MonthSensor(SensorEntity):
    def __init__(self, hg_user):
        self._state = None
        self._month_stats = {}
        self._hg_user = hg_user

    @property
    def name(self):
        return 'HoneyGain Month'

    @property
    def unique_id(self):
        return f"honeygain_month_stats"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._month_stats
    
    def update(self):
        try:
            statsMonth = self._hg_user.stats()
            credits_total = 0.0
            gather_top_credit = []
            gather_top_traffic = []
            content_top = []
            referrals_top = []
            winnings_top = []
            other_top = []
            first = True

            for key, value in statsMonth.items():
                credits_total += float(value["gathering"]["credits"]) 
                credits_total += float(value["content_delivery"]["credits"]) 
                credits_total += float(value["referrals"]["credits"]) 
                credits_total += float(value["winnings"]["credits"]) 
                credits_total += float(value["other"]["credits"])

                day = {
                    "gather": value["gathering"],
                    "content": value["content_delivery"],
                    "referrals": value["referrals"],
                    "winnings": {
                        "credits": value["winnings"]["credits"]
                    },
                    "other": {
                        "credits": value["other"]["credits"]
                    }
                }

                if(first):
                    gather_top_credit = [
                        day["gather"]["credits"]
                        ]
                    gather_top_traffic = [
                        day["gather"]["traffic"]
                        ]
                    content_top = [day["content"]["credits"]]
                    referrals_top = [day["referrals"]["credits"]]
                    winnings_top = [day["winnings"]["credits"]]
                    other_top = [day["other"]["credits"]]
                    first = False

                if(gather_top_credit[0] < day["gather"]["credits"]):
                    gather_top_credit = [
                        day["gather"]["credits"]
                        ]
                    gather_top_traffic = [
                        day["gather"]["traffic"]
                        ]

                if(content_top[0] < day["content"]["credits"]):
                    content_top = [
                        day["content"]["credits"],
                        day["content"]["time"]
                        ]

                if(referrals_top[0] < day["referrals"]["credits"]):
                    referrals_top = [day["referrals"]["credits"]]

                if(winnings_top[0] < day["winnings"]["credits"]):
                    winnings_top = [day["winnings"]["credits"]]

                if(other_top[0] < day["other"]["credits"]):
                    other_top = [day["other"]["credits"]]

            self._month_stats = {
                "gather credit": gather_top_credit,
                "gather traffic": gather_top_traffic,
                "content": content_top,
                "referrals": referrals_top,
                "winnings": winnings_top,
                "other": other_top
            }
            self._state = credits_total
        except:
            _LOGGER.error("Error while getting month data")

class BalanceSensor(SensorEntity):
    def __init__(self, hg_user):
        self._state = None
        self._balance = {}
        self._hg_user = hg_user

    @property
    def name(self):
        return 'HoneyGain Balance'

    @property
    def unique_id(self):
        return f"honeygain_balance"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._balance
    
    def update(self):
        try:
            myData = self._hg_user.balances()

            self._balance = {
                "realtime credits": myData["realtime"]["credits"],
                "realtime cents": myData["realtime"]["usd_cents"],
                "payout credits": myData["payout"]["credits"],
                "payout cents": myData["payout"]["usd_cents"],
                "min credits": myData["min_payout"]["credits"],
                "min cents": myData["min_payout"]["usd_cents"],
            }
            self._state = myData["payout"]["usd_cents"]
        except:
            _LOGGER.error("Error while getting user data")

