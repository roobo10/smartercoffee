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
		default_coffee_scene = SCScene(s)
		scene_items.append(default_coffee_scene)

		for c in sc.SC_CONFIG['smartercoffee']['presets']:
			cups = sc.SC_CONFIG['smartercoffee']['presets'][c]['cups']
			strength = sc.SC_CONFIG['smartercoffee']['presets'][c]['strength']

			logging.info("SmarterCoffee Preset: Cups - %d; Strength - %d." % (cups,strength))
			coffee_scene = SCScene(s,cups=cups,strength=strength)
			scene_items.append(coffee_scene)

		add_devices(scene_items)

		sc.SC_SCENES = [item.entity_id for item in scene_items]
		sc.SC_SCENE_GROUP = group.Group.create_group(hass, "Make Coffee", sc.SC_SCENES)


class SCScene(Scene):
	def __init__(self, sc, cups=None, strength=None):
		self._sc = sc
		self.cups = cups
		self.strength = strength

	@property
	def entity_id(self):
		id = "scene.sc_make_with_current"
		if self.cups is not None:
			id = "scene.sc_make_%d_%d" % (self.cups, self.strength)
		return id

	@property
	def name(self):
		name = "Make Coffee with Current Settings"
		if self.cups is not None:
			name = "Make %d Cups of %s Coffee" % (self.cups,self._sc.coffee_strength_text[self.strength])
		return name

	@property
	def icon(self):
		return "mdi:coffee-to-go"

	@property
	def state(self):
		"""Return the state of the scene."""
		return True

	def activate(self):
		logging.info("Making some coffee...")
		if self.cups is None:
			logging.info("Making Coffee with Current Settings")
			self._sc.start_with_current_settings()
		else:
			logging.info("Making %d Cups of %s Coffee." % (self.cups, self._sc.coffee_strength_text[self.strength].title()))
			self._sc.start_with_settings(self.cups, self.strength, 5, True)
		return True
