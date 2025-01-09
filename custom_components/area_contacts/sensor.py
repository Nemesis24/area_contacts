import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.core import callback
from homeassistant.helpers import entity_registry, area_registry, device_registry
from .const import DOMAIN, ATTR_COUNT, ATTR_TOTAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    excluded = entry.data.get("excluded_entities", [])
    
    _LOGGER.debug("Starting Area Contacts configuration")
    _LOGGER.debug(f"Excluded entities: {excluded}")
    
    area_reg = area_registry.async_get(hass)
    entity_reg = entity_registry.async_get(hass)
    device_reg = device_registry.async_get(hass)
    
    areas = area_reg.async_list_areas()
    _LOGGER.debug(f"Found areas: {[area.name for area in areas]}")
    
    sensors = []
    all_contacts = set()
    
    for area in areas:
        area_contacts = set()
        area_excluded = set()
        
        for entity in entity_reg.entities.values():
            if entity.entity_id.startswith("binary_sensor.") and entity.entity_id.endswith("_contact") and entity.area_id == area.id:
                if entity.entity_id not in excluded:
                    area_contacts.add(entity.entity_id)
                    _LOGGER.debug(f"Contact {entity.entity_id} found directly in {area.name}")
                else:
                    area_excluded.add(entity.entity_id)
        
        for device_id in device_reg.devices:
            device = device_reg.async_get(device_id)
            if device and device.area_id == area.id:
                for entity in entity_reg.entities.values():
                    if entity.device_id == device_id and entity.entity_id.startswith("binary_sensor.") and entity.entity_id.endswith("_contact"):
                        if entity.entity_id not in excluded:
                            area_contacts.add(entity.entity_id)
                            _LOGGER.debug(f"Contact {entity.entity_id} found via device in {area.name}")
                        else:
                            area_excluded.add(entity.entity_id)
        
        if area_contacts:
            _LOGGER.debug(f"Area {area.name}: {len(area_contacts)} contacts found: {area_contacts}")
            sensors.append(RoomContactsSensor(area.name, list(area_contacts), list(area_excluded)))
            all_contacts.update(area_contacts)
        else:
            # Supprimer l'entité de commutateur si la pièce n'a plus de capteurs contact
            sensor_contact_entity_id = f"sensor.contacts_{area.name.lower().replace(' ', '_')}"
            entity = entity_reg.async_get(sensor_contact_entity_id)
            if entity:
                _LOGGER.debug(f"Removing switch entity for area with no contact sensors: {sensor_contact_entity_id}")
                entity_reg.async_remove(sensor_contact_entity_id)

    if all_contacts:
        _LOGGER.debug(f"Total contacts found: {len(all_contacts)}")
        sensors.append(AllContactsSensor(list(all_contacts), excluded)) 
    
    _LOGGER.debug(f"Creating {len(sensors)} sensors")
    async_add_entities(sensors)

class RoomContactsSensor(SensorEntity):
    def __init__(self, room_name, contacts, excluded_contacts):
        self._room = room_name
        self._contacts = contacts
        self._excluded_contacts = excluded_contacts
        self._attr_name = f"Contacts {room_name}"
        self._attr_unique_id = f"area_contacts_{room_name.lower().replace(' ', '_')}"
        self._state = STATE_OFF
        self._count = 0
        self._total = len(contacts)
        self._contacts_open = []
        self._contacts_closed = []
        _LOGGER.debug(f"Initializing sensor {self._attr_name} with {self._total} contacts: {self._contacts}")

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return "mdi:door-open" if self._state == STATE_ON else "mdi:door-closed"

    @property
    def extra_state_attributes(self):
        return {
            "count": self._count,
            "of": self._total,
            "count_of": f"{self._count}/{self._total}",
            "contacts_open": self._contacts_open,
            "contacts_closed": self._contacts_closed,
            "excluded_contacts": self._excluded_contacts,
        }

    async def async_added_to_hass(self):
        @callback
        def async_state_changed(*_):
            self.async_schedule_update_ha_state(True)

        for contact in self._contacts:
            self.async_on_remove(
                self.hass.helpers.event.async_track_state_change(
                    contact, async_state_changed
                )
            )
        
        self.async_schedule_update_ha_state(True)

    async def async_update(self):
        self._count = 0
        self._contacts_open = []
        self._contacts_closed = []
        
        for contact_id in self._contacts:
            state = self.hass.states.get(contact_id)
            if state:
                if state.state == STATE_ON:
                    self._count += 1
                    self._contacts_open.append(contact_id)
                else:
                    self._contacts_closed.append(contact_id)
        
        self._state = STATE_ON if self._count > 0 else STATE_OFF
        _LOGGER.debug(f"Updating {self._attr_name}: {self._count}/{self._total} contacts open")

class AllContactsSensor(RoomContactsSensor):
    def __init__(self, contacts, excluded_contacts):
        super().__init__("All", contacts, excluded_contacts)
        self._attr_name = "All Area Contacts"
        self._attr_unique_id = "area_contacts_all"
