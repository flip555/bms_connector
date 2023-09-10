from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .seplos_helper import send_serial_command, extract_data_from_message

# Define your two commands to be sent
COMMAND_1 = "~200046420000FDAE\r"
COMMAND_2 = "~200046440000FDAC\r"

class SeplosBMSSensorBase(CoordinatorEntity):
    """Base class for Seplos BMS sensors."""

    def __init__(self, coordinator, port, attribute, name, unit=None, icon=None):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._port = port
        self._attribute = attribute
        self._name = name
        self._unit = unit
        self._icon = icon

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Seplos BMS {self._name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return getattr(self.coordinator.data, self._attribute, None)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Seplos BMS sensor platform."""

    port = entry.data.get("usb_port")  # Get port from the config entry

    async def async_update_data():
        """Fetch data from Seplos BMS."""
        response1 = await hass.async_add_executor_job(send_serial_command, COMMAND_1, port)
        telemetry, _ = extract_data_from_message(response1)

        response2 = await hass.async_add_executor_job(send_serial_command, COMMAND_2, port)
        _, alarms = extract_data_from_message(response2)

        return telemetry  # For now, just returning telemetry as an example

    coordinator = DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        name="seplos_bms_sensor",
        update_method=async_update_data,
        update_interval=timedelta(seconds=30),  # Define how often to fetch data
    )

    await coordinator.async_refresh()  # Fetch data once before adding entities

    # Define sensors
    sensors = [
        SeplosBMSSensorBase(coordinator, port, "current", "Current", "A"),
        SeplosBMSSensorBase(coordinator, port, "voltage", "Voltage", "V"),
        # ... Add other sensors here based on the telemetry data attributes ...
    ]

    async_add_entities(sensors, True)
