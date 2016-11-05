# smartercoffee

Smartercoffee.py is a module written in Python 3 to control the Smarter Coffee Machine over wifi.

# Home Assistant

Copy the files to the '''custom_components''' directory in the Home Assistant configuration directory.

In your configuration.yaml file add:

    smartercoffee:
      ip: [Coffee Maker IP Address]
      presets:
        one:
          cups: 2
          strength: 0
        two:
          cups: 4
          strength: 2
