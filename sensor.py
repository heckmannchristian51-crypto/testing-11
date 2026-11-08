import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

DOMAIN = "bosmon_alarm"

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType = None
) -> None:
    """Richtet den BosMon Sensor ein."""
    sensor = BosMonAlarmSensor()
    async_add_entities([sensor])

    # Registriert den Dienst 'bosmon_alarm.trigger_alarm'
    async def handle_alarm(call):
        message = call.data.get("message", "Unbekannter Alarm")
        ric = call.data.get("ric", "0000000")
        sensor.update_alarm(message, ric)

    hass.services.async_register(DOMAIN, "trigger_alarm", handle_alarm)

class BosMonAlarmSensor(SensorEntity):
    """Der Sensor, der den Alarm in HA anzeigt."""

    def __init__(self):
        self._state = "Kein Alarm"
        self._attributes = {"ric": "-", "zeit": "-"}

    @property
    def name(self):
        return "BosMon Letzter Alarm"

    @property
    def unique_id(self):
        return "bosmon_alarm_letzter_alarm"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update_alarm(self, message, ric):
        """Aktualisiert den Zustand, wenn BosMon Daten sendet."""
        self._state = message
        self._attributes = {
            "ric": ric,
            "zeit": datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        }
        self.schedule_update_ha_state()
