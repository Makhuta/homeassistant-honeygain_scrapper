import sys
from pyHoneygain import HoneyGain, NotLoggedInError
from datetime import datetime
import time
from typing import Dict, Any

from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.const import CONF_NAME, CONF_USERNAME, CONF_PASSWORD

def stats_parser(stats: Dict[str, Any]) -> list:
    output = []
    for key, value in stats.items():
        if type(value) == dict:
            value["date"] = key
            output.append(value)
    
    return output

def statsToday_parser(statsToday: Dict[str, Any]) -> Dict[str, Any]:
    if "total" in statsToday:
        del statsToday["total"]
    if "winning" in statsToday:
        del statsToday["winning"]
    if "referral" in statsToday:
        del statsToday["referral"]
    if "other" in statsToday:
        del statsToday["other"]
    if "cdn" in statsToday:
        statsToday["cdn_credits"] = statsToday["cdn"]["credits"]
        statsToday["cdn_seconds"] = statsToday["cdn"]["seconds"]
        del statsToday["cdn"]
    if "gathering" in statsToday:
        statsToday["gathering_credits"] = statsToday["gathering"]["credits"]
        del statsToday["gathering"]
    return statsToday

def statsTodayJT_parser(statsTodayJT: Dict[str, Any]) -> Dict[str, Any]:
    if "total" in statsTodayJT:
        statsTodayJT["total_credits"] = statsTodayJT["total"]["credits"]
        del statsTodayJT["total"]
    if "winning" in statsTodayJT:
        statsTodayJT["winning_credits"] = statsTodayJT["winning"]["credits"]
        del statsTodayJT["winning"]
    if "referral" in statsTodayJT:
        statsTodayJT["referral_credits"] = statsTodayJT["referral"]["credits"]
        del statsTodayJT["referral"]
    if "other" in statsTodayJT:
        statsTodayJT["other_credits"] = statsTodayJT["other"]["credits"]
        del statsTodayJT["other"]
    if "bonus" in statsTodayJT:
        statsTodayJT["bonus_credits"] = statsTodayJT["bonus"]["credits"]
        del statsTodayJT["bonus"]
    if "cdn" in statsTodayJT:
        statsTodayJT["cdn_credits"] = statsTodayJT["cdn"]["credits"]
        statsTodayJT["cdn_seconds"] = statsTodayJT["cdn"]["seconds"]
        del statsTodayJT["cdn"]
    if "gathering" in statsTodayJT:
        statsTodayJT["gathering_credits"] = statsTodayJT["gathering"]["credits"]
        statsTodayJT["gathering_bytes"] = statsTodayJT["gathering"]["bytes"]
        del statsTodayJT["gathering"]

    return statsTodayJT

def isDifferentDay(date1: str, date2: str) -> bool:
    dateA = datetime.strptime(date1, "%Y-%d-%m")
    dateB = datetime.strptime(date2, "%Y-%d-%m")

    return (dateA.day != dateB.day) or (dateA.month != dateB.month) or (dateA.year != dateB.year)

def load_honeypot(status):
    if "progress_bytes" in status and "max_bytes" in status and "winning_credits" in status:
        return {
            "success": False,
            "can_open": int(status["progress_bytes"]) == int(status["max_bytes"]),
            "credits": 0.0
        }


        #if int(status["progress_bytes"]) == int(status["max_bytes"] and status["max_bytes"]):

    return {
        "success": False,
        "can_open": False,
        "credits": 0.0
    }


class HG_Api:
    def __init__(self, hass: HomeAssistantType, username: CONF_USERNAME, password: CONF_PASSWORD):
        self.username = username
        self.password = password
        self.hass = hass
        self.user = HoneyGain()

    def userLogin(self) -> None:
        try:
            self.user.login(self.username, self.password)
        except:
            raise FailedToLogin

    def updateData(self) -> Dict[str, Any]:
        data = {}
        functions = {
            "me": self.user.me,
            "devices": self.user.devices,
            "stats": lambda: (stats_parser(self.user.stats())),
            "stats_today": lambda: (statsToday_parser(self.user.stats_today())),
            "stats_today_jt": lambda: (statsTodayJT_parser(self.user.stats_today_jt())),
            "notifications": self.user.notifications,
            "payouts": self.user.payouts,
            "balances": self.user.balances,
            "honeypot": self.user.get_honeypot_status
        }

        for (key, function) in functions.items():
            try:
                data[key] = function()
            except NotLoggedInError:
                self.userLogin()
                try:
                    data[key] = function()
                except:
                    raise LoginBrokeDown
            except:
                raise UnknownError

        return data

    def openHoneyPot(self, honeyPot_info: Dict[str, Any]) -> Dict[str, Any]:
        opened = False
        if "progress_bytes" in honeyPot_info and "max_bytes" in honeyPot_info and "winning_credits" in honeyPot_info:
            if int(honeyPot_info["progress_bytes"]) == int(honeyPot_info["max_bytes"]) and honeyPot_info["winning_credits"] is None:
                try:
                    reward = self.user.open_honeypot()
                except NotLoggedInError:
                    self.userLogin()
                    try:
                        reward = self.user.open_honeypot()
                    except:
                        raise LoginBrokeDown
                except:
                    raise UnknownError
                if reward["success"]:
                    opened = True
        
        return opened

class FailedToLogin(Exception):
    "Raised when the HoneyGain user fail to Log-in"
    pass

class LoginOnCooldown(Exception):
    "Raised when the HoneyGain user Log-in is on cooldown"
    pass

class LoginBrokeDown(Exception):
    "Raised when the HoneyGain user Log-in broke try to relog"
    pass

class UnknownError(Exception):
    "Raised when the HoneyGain user Log-in broke try to relog"
    pass