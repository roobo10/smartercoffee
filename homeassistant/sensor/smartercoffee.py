from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity import generate_entity_id
#import homeassistant.loader as loader
import custom_components.smartercoffee as sc

import logging
import smartercoffee
import calendar
import time

DEPENDENCIES = ['smartercoffee','group']

def setup_platform(hass, config, add_devices, discovery_info=None):
	logging.info("Loading SmarterCoffee Sensor platform")
	if sc.SC_SERVER is None:
		return

	s = sc.SC_SERVER
	logging.info("Loading SmarterCoffee platform")
	if len(sc.SC_SENSORS) <= 4:
		sensors = [SCCups(s),SCWater(s),SCStrength(s),SCStatus(s)]
		add_devices(sensors)


class SCCups(Entity):
	def __init__ (self, sc):
		self._sc = sc

	@property
	def name(self):
		"""Return the name of the sensor."""
		return 'SC Cups'

	@property
	def icon(self):
		return "mdi:coffee"

	@property
	def state(self):
		"""Return the state of the sensor."""
		try:
			return self._sc.cups
		except:
			return 0

	@property
	def unit_of_measurement(self):
		"""Return the unit of measurement."""
		return "Cups"

class SCWater(Entity):
	def __init__ (self, sc):
		self._sc = sc

	@property
	def name(self):
		"""Return the name of the sensor."""
		return 'SC Water'

	@property
	def icon(self):
		return "mdi:water"

	@property
	def state(self):
		"""Return the state of the sensor."""
		try:
			return self._sc.water_level_text[self._sc.water_level]
		except:
			return "N/A"

	@property
	def unit_of_measurement(self):
		"""Return the unit of measurement."""
		return None

class SCStrength(Entity):
	def __init__ (self, sc):
		self._sc = sc

	@property
	def name(self):
		"""Return the name of the sensor."""
		return 'SC Strength'

	@property
	def icon(self):
		return "mdi:speedometer"

	@property
	def state(self):
		"""Return the state of the sensor."""
		try:
			return self._sc.coffee_strength_text[self._sc.coffee_strength]
		except:
			return "N/A"

	@property
	def unit_of_measurement(self):
		"""Return the unit of measurement."""
		return None

class SCStatus(Entity):
	def __init__ (self, sc):
		self._sc = sc

	@property
	def name(self):
		"""Return the name of the sensor."""
		return 'SC Status'

	@property
	def icon(self):
		return "mdi:information"

	@property
	def state(self):
		"""Return the state of the sensor."""
		try:
			return self._sc.state
		except:
			return "N/A"

	@property
	def unit_of_measurement(self):
		"""Return the unit of measurement."""
		return None
