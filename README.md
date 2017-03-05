# smartercoffee

Smartercoffee.py is a module written in Python 3 to control the Smarter Coffee Machine over wifi.

## What does this module do?

The smartercoffee module can:

* Automatically check the status of a smarter coffee machine every 15 minutes.
* Make a coffee with the default settings
* Make a coffee with custom settings

## How do I use it


Import the module:

```python
import smartercoffee
```

Create an instance of SmarterCoffee and start the client with a misleading function name:

```python
    s = smartercoffee.SmarterCoffee(COFFEE_MACHINE_IP)
    s.start_server()
```

Create a callback function to receive updates:

```python
    s.watch_updates(callback_function)
```

To make a coffee with default settings:
```python
    s.start_with_current_settings()
```
To use custom settings:
```python
    s.start_with_settings(CUPS, STRENGTH, HOTPLATE, GRINDER)
```

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
