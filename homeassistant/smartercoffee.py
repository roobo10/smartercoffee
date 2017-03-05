#from homeassistant.components.discovery import load_platform
from homeassistant.helpers.discovery import load_platform
import smartercoffee
import logging
import time

DEPENDENCIES = ['group']

DOMAIN = 'smartercoffee'
SC_SERVER = None
G_HASS = None
SC_CONFIG = None
SC_SENSORS = []
SC_SCENES = []
SC_SCENE_GROUP = None
def load_subcomponents():
    global DOMAIN
    global SC_SERVER
    global LWHUB
    global SC_CONFIG
    global SC_SENSORS
    global SC_SCENES
    global SC_SCENE_GROUP
    load_platform(G_HASS, 'sensor', DOMAIN)
    load_platform(G_HASS, 'scene', DOMAIN)


def setup(hass, config):
    """Your controller/hub specific code."""
    global SC_SERVER
    global G_HASS
    global SC_CONFIG

    SC_CONFIG = config
    G_HASS = hass
    logging.info("Setting up SmarterCoffee with IP %s" % config['smartercoffee']['ip'])
    if SC_SERVER is None:
        s = smartercoffee.SmarterCoffee(config['smartercoffee']['ip'])
        s.start_server()
        SC_SERVER = s

    load_subcomponents()

    return True
