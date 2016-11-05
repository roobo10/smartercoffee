from homeassistant.const import TEMP_CELSIUS
from homeassistant.components.scene import Scene
import homeassistant.components.group as group
from homeassistant.helpers.entity import generate_entity_id
import custom_components.smartercoffee as sc

import logging
import smartercoffee
import calendar
import time

DEPENDENCIES = ['smartercoffee','group']

def setup_platform(hass, config, add_devices, discovery_info=None):

	logging.info("Loading SmarterCoffee Scene platform")

	if sc.SC_SERVER is None:
		return

	s = sc.SC_SERVER

	scene_items = []
	if len(sc.SC_SCENES) == 0:
		scene_items.append(SCScene(s))

		for c in sc.SC_CONFIG['smartercoffee']['presets']:
			logging.info(c)
			cups = sc.SC_CONFIG['smartercoffee']['presets'][c]['cups']
			strength = sc.SC_CONFIG['smartercoffee']['presets'][c]['strength']

			logging.info("SmarterCoffee Preset: Cups - %d; Strength - %d." % (cups,strength))
			scene_items.append(SCScene(s,cups=cups,strength=strength))

		add_devices(scene_items)
		sc.SC_SCENES = [item.entity_id for item in scene_items]
		sc.SC_SCENE_GROUP = group.Group.create_group(hass, "Make Coffee", sc.SC_SCENES)


class SCScene(Scene):
	def __init__(self, sc, cups=-1, strength=-1):
		self._sc = sc
		self.cups = cups
		self.strength = strength

	@property
	def entity_id(self):
		if self.cups == -1:
			return "scene.sc_make_with_current"
		else:
			return "scene.sc_make_%s_cups_%s" % (str(self.cups),self._sc.coffee_strength_text[self.strength])

	@property
	def name(self):
		if self.cups == -1:
			return "Make Coffee with Current Settings"
		else:
			return "Make %s Cups of %s Coffee" % (str(self.cups),self._sc.coffee_strength_text[self.strength])

	@property
	def icon(self):
		return "mdi:coffee-to-go"

	@property
	def state(self):
		"""Return the state of the scene."""
		return True

	def activate(self):
		if self.cups == -1:
			self._sc.start_with_current_settings()
		else:
			self._sc.start_with_settings(self.cups, self.strength, 5, True)
		return True
