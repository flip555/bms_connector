
from homeassistant.components.number import NumberEntity

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    # Add your number setup code here
    # Example:
    async_add_entities([YourNumberClass(entry)], True)

class YourNumberClass(NumberEntity):

    def __init__(self, entry):
        self._entry = entry
        self._value = None
        self._min_value = 0
        self._max_value = 100
        self._step = 1

    @property
    def name(self):
        return "Your Number Name"

    @property
    def state(self):
        return self._value

    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value

    @property
    def step(self):
        return self._step

    async def async_set_value(self, value):
        self._value = value
        # Add your code to handle the number value here
        # Example:
        pass
