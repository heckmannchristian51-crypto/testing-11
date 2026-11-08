import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)
DOMAIN = "bosmon_alarm"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Setzt die BosMon Integration auf."""
    hass.data[DOMAIN] = {}
    return True
