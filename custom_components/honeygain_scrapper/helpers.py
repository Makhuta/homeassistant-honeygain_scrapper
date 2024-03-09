import re
import unicodedata
from typing import Any, Dict


from .hg_api import HG_Api

from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD


def setup_client(hass: HomeAssistantType, username: CONF_USERNAME, password: CONF_PASSWORD) -> HG_Api:
    client = HG_Api(hass, username, password)
    client.userLogin()

    return client

def convert_objects(object: Dict[str, Any]) -> Dict[str, Any]:
    data = {}
    for key in object:
        item = object[key]
        if type(item) == dict:
            data[key] = [convert_objects(item)]
        else:
            data[key] = item
    return data

def sanitize_text(input_text):
    lowercase_text = str(input_text).lower()
    normalized_text = ''.join(c for c in unicodedata.normalize('NFD', lowercase_text) if unicodedata.category(c) != 'Mn')
    sanitized_text = re.sub(r'[^a-zA-Z0-9_]', '_', normalized_text)

    return sanitized_text