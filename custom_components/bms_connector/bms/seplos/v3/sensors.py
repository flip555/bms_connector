from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.entity import DeviceInfo

from .data_parser import extract_data_from_message, build_commands_for_address
from ....connector import get_serial_send_function
import asyncio
import logging
from datetime import timedelta
from ....const import (
    NAME,
    DOMAIN,
    VERSION,
    ATTRIBUTION,
)
from .const import (
    ALARM_ATTRIBUTES,
    ALARM_MAPPINGS,
    SYSTEM_ATTRIBUTES,
    SETTINGS_ATTRIBUTES,
)

_LOGGER = logging.getLogger(__name__)

# Sentinel pour distinguer "attribut absent" (→ chercher dans l'objet suivant)
# de "attribut présent mais valant 0" (valeur numérique valide à retourner)
_MISSING = object()


# ---------------------------------------------------------------------------
# generate_sensors
# ---------------------------------------------------------------------------

async def generate_sensors(hass, bms_type, connector_info, config_battery_address,
                            sensor_prefix, entry_id, async_add_entities):
    """
    Génère et enregistre tous les capteurs pour UNE adresse de batterie.

    config_battery_address doit être un entier (ex: 1 pour l'adresse Modbus 0x01).
    Pour ajouter une seconde batterie, appeler generate_sensors une deuxième fois
    avec config_battery_address=2 (et un sensor_prefix différent si désiré).
    """

    # ------------------------------------------------------------------
    # Classe dérivée pour les capteurs calculés
    # ------------------------------------------------------------------

    class DerivedSeplosBMSSensor(SeplosBMSSensorBase):
        def __init__(self, *args, **kwargs):
            self._calc_function = kwargs.pop("calc_function", None)
            super().__init__(*args, **kwargs)
            self._config_battery_address = config_battery_address

        @property
        def state(self):
            if self._calc_function:
                result = self._calc_function(self.coordinator.data)
                _LOGGER.debug("Derived sensor '%s' calculated value: %s", self._name, result)
                return result
            return super().state

    # ------------------------------------------------------------------
    # Fonction de mise à jour
    # ------------------------------------------------------------------

    async def async_update_data():
        """
        Interroge la batterie via le bus RS485 en utilisant son adresse Modbus
        propre (config_battery_address), puis parse les réponses.

        IMPORTANT : on n'utilise PAS l'adresse 0x00 (broadcast) qui ferait
        répondre toutes les batteries simultanément et créerait des collisions
        sur le bus RS485.
        """
        # Conversion en int si l'adresse est passée en string
        if isinstance(config_battery_address, str):
            try:
                addr_int = int(config_battery_address, 0)  # accepte "1", "0x01", etc.
            except ValueError:
                addr_int = 1
                _LOGGER.warning(
                    "config_battery_address '%s' invalide, utilisation de l'adresse par défaut 1",
                    config_battery_address
                )
        else:
            addr_int = int(config_battery_address)

        # Construction des commandes Modbus RTU avec la bonne adresse
        # (remplace les anciennes commandes hardcodées avec adresse 0x00)
        commands = build_commands_for_address(addr_int)
        _LOGGER.debug(
            "Interrogation batterie 0x%02X : PIA=%s | PIB=%s",
            addr_int, commands[0], commands[1]
        )

        # Envoi série (bloquant, exécuté dans un thread executor)
        send_func = get_serial_send_function(connector_info)
        telemetry_data_str = await hass.async_add_executor_job(
            send_func, commands
        )

        # Parsing des réponses
        battery_address, pia, pib, system_details, protection_settings = \
            extract_data_from_message(
                telemetry_data_str,
                telemetry_requested=True,
                teledata_requested=True,
                debug=True,
                config_battery_address=addr_int,
            )

        return battery_address, pia, pib, system_details, protection_settings

    # ------------------------------------------------------------------
    # Premier appel pour initialiser le coordinator
    # ------------------------------------------------------------------

    battery_address, telemetry, alarms, system_details, protection_settings = \
        await async_update_data()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"seplos_bms_sensor_{config_battery_address}",
        update_method=async_update_data,
        update_interval=timedelta(seconds=5),
    )

    _LOGGER.debug("async_refresh data generate_sensors called (addr=%s)", config_battery_address)
    await coordinator.async_refresh()

    # ------------------------------------------------------------------
    # Définition des capteurs PIA (pack global)
    # ------------------------------------------------------------------

    pia_sensors = [
        SeplosBMSSensorBase(
            coordinator, connector_info, "pack_voltage",
            "Pack Voltage", "V", "mdi:flash-circle",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "current",
            "Current", "A", "mdi:current-ac",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "remaining_capacity",
            "Remaining Capacity", "Ah", "mdi:battery-charging-wireless",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "total_capacity",
            "Total Capacity", "Ah", "mdi:battery",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "total_discharge_capacity",
            "Total Discharge Capacity", "Ah", "mdi:battery-discharging",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "soc",
            "State of Charge", "%", "mdi:gauge",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "soh",
            "State of Health", "%", "mdi:gauge",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "cycle",
            "Cycle", "", "mdi:numeric",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "avg_cell_voltage",
            "Avg Cell Voltage", "V", "mdi:battery-20",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "avg_cell_temperature",
            "Avg Cell Temperature", "°C", "mdi:thermometer",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "max_cell_voltage",
            "Max Cell Voltage", "V", "mdi:battery-high",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "min_cell_voltage",
            "Min Cell Voltage", "V", "mdi:battery-low",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "max_cell_temperature",
            "Max Cell Temperature", "°C", "mdi:thermometer-chevron-up",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "min_cell_temperature",
            "Min Cell Temperature", "°C", "mdi:thermometer-chevron-down",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "max_discharge_current",
            "Max Discharge Current", "A", "mdi:current-dc",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "max_charge_current",
            "Max Charge Current", "A", "mdi:current-dc",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
    ]

    # ------------------------------------------------------------------
    # Définition des capteurs PIB (cellules individuelles)
    # ------------------------------------------------------------------

    pib_sensors = [
        SeplosBMSSensorBase(
            coordinator, connector_info, f"cell{i}_voltage",
            f"Cell {i} Voltage", "V", "mdi:battery",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        )
        for i in range(1, 17)
    ] + [
        SeplosBMSSensorBase(
            coordinator, connector_info, "cell_temperature_1",
            "Cell Temperature 1", "°C", "mdi:thermometer",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "cell_temperature_2",
            "Cell Temperature 2", "°C", "mdi:thermometer",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "cell_temperature_3",
            "Cell Temperature 3", "°C", "mdi:thermometer",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "cell_temperature_4",
            "Cell Temperature 4", "°C", "mdi:thermometer",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "environment_temperature",
            "Environment Temperature", "°C", "mdi:thermometer-lines",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
        SeplosBMSSensorBase(
            coordinator, connector_info, "power_temperature",
            "Power Temperature", "°C", "mdi:thermometer-lines",
            battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id
        ),
    ]

    sensors = pia_sensors + pib_sensors
    async_add_entities(sensors, True)


# ---------------------------------------------------------------------------
# Classe de base des capteurs
# ---------------------------------------------------------------------------

class SeplosBMSSensorBase(CoordinatorEntity):
    """Capteur de base pour un attribut d'une batterie SEPLOS V3."""

    def interpret_alarm(self, event, value):
        flags = ALARM_MAPPINGS.get(event, [])
        if not flags:
            return f"Unknown event: {event}"
        triggered_alarms = [
            flag for idx, flag in enumerate(flags)
            if value is not None and value & (1 << idx)
        ]
        return ', '.join(triggered_alarms) if triggered_alarms else "No Alarm"

    def __init__(self, coordinator, port, attribute, name, unit=None,
                 icon=None, battery_address=None, sensor_prefix=None, entry_id=None):
        super().__init__(coordinator)
        self._port = port
        self._attribute = attribute
        self._name = name
        self._unit = unit
        self._icon = icon
        self._battery_address = battery_address
        self._sensor_prefix = sensor_prefix
        self._entry_id = entry_id
        
        # Device info for V3 BMS
        self._attr_device_info = DeviceInfo(
            identifiers={("bms_connector", f"seplos_v3_{entry_id}")},
            name=f"{sensor_prefix}",
            manufacturer="Seplos",
            model="V3 BMS",
            sw_version="Unknown",
        )
        self._entry_id = entry_id

    @property
    def name(self):
        prefix = f"{self._sensor_prefix} - {self._battery_address} -"
        return f"{prefix} {self._name}"

    @property
    def unique_id(self):
        return f"bms_connector_v3_{self._entry_id}_{self._name}"

    @property
    def state(self):
        if not self._attribute:
            return super().state

        value = _MISSING

        if isinstance(self.coordinator.data, tuple):
            battery_address_data, pia_data, pib_data, system_details_data, protection_settings_data = \
                self.coordinator.data
            # Cherche dans PIA, puis PIB, puis les autres objets
            # Utilise _MISSING comme sentinel pour distinguer "absent" de "valeur 0"
            for data_obj in (pia_data, pib_data, system_details_data, protection_settings_data):
                result = self.get_value(data_obj)
                if result is not _MISSING:
                    value = result
                    break
        else:
            value = self.get_value(self.coordinator.data)

        if value is _MISSING or value is None or value == '':
            if self._attribute == 'current':
                _LOGGER.debug(
                    "current est None, retour à 0.00 pour éviter 'unknown' dans HA"
                )
                return 0.00
            _LOGGER.warning("Aucune donnée trouvée pour %s", self._name)
            return None

        _LOGGER.debug("État du capteur %s : %s", self._name, value)
        return value

    @property
    def unit_of_measurement(self):
        return self._unit

    def get_value(self, data_object):
        """
        Récupère la valeur d'un attribut depuis un objet de données.

        Retourne _MISSING si l'objet est None ou si l'attribut n'existe pas
        dans cet objet — ce qui permet à state() de continuer à chercher
        dans l'objet suivant (PIA → PIB → ...).

        Retourne la valeur réelle (y compris 0, 0.0, False) si l'attribut
        existe, afin de ne pas confondre "zéro" avec "absent".
        """
        if data_object is None:
            return _MISSING

        # Accès à une liste par index : ex "cell_voltages[0]"
        if '[' in self._attribute and ']' in self._attribute:
            attr, index_str = self._attribute.split('[')
            index = int(index_str.rstrip(']'))
            list_data = getattr(data_object, attr, _MISSING)
            if list_data is _MISSING:
                return _MISSING
            if index < len(list_data):
                return list_data[index]
            return _MISSING

        # Vérifier si l'attribut existe dans cet objet précis
        if not hasattr(data_object, self._attribute):
            return _MISSING

        return getattr(data_object, self._attribute)

    @property
    def icon(self):
        return self._icon
