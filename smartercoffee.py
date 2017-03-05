import socket
from queue import Queue
import threading
import logging
import binascii
import time

class SmarterCoffee:
	_port = 2081
	_ip = ''
	_received_commands = Queue()
	_observers = []
	_device = None
	_last_update_data = None
	error = None

	water_level_number = {
		'0x2'  : 0,
		'0x0'  : 1,
		'0x1'  : 2,
		'0x11' : 3,
		'0x12' : 4,
		'0x13' : 5
	}
	water_level_text = ["Insufficient Water","Very Low","Low","Half","Half 1","Full"]

	coffee_strength_text = ["Weak","Medium","Strong"]

	responses_text = ["OK","Brewing Error","","Insufficient Water","Command does not exist","No Carafe"]

	def watch_updates(self, callback):
		self._observers.append(callback)
		return True

	def __init__(self, ip_address):
		self._ip = ip_address

		self.device_message = None
		self.status_message = None
		self.water_level = None
		self.wifi_strength = None
		self.coffee_strength = None
		self.cups = None

		self._device = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
		self._device.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		self._device.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self._connected = False

	def start_server (self):
		t = threading.Thread(target=self._server, args=(self._received_commands,))
		# classifying as a daemon, so they will die when the main dies
		t.daemon = True
		# begins, must come after daemon definition
		t.start()

	def _server(self, received_commands):
		while True:
			if not self._connected:
				self._device.connect((self._ip, self._port))
				self._connected = True
				running_time = time.time()

				while True and running_time + 120 > time.time():
					data = self._device.recv(4096) # buffer size is 1024 bytes
					hex_data = list(map(hex, data))
					self.process_command(hex_data)
					logging.debug("Hex Data: {}".format(hex_data))

				self._device.shutdown(socket.SHUT_RDWR)
				self._device.close()
				self._connected = False
				time.sleep(900)

	def process_command(self, data):
		if len(data) == 7:
			changed = False
			changed = True if self._last_update_data != data else False

			if changed:
				self._last_update_data = data

				status = int(data[1],16)
				self.grinder = True if (status & 2) else False
				self.carafe = True if (status & 1) else False
				self.hotplate = True if (status & 56) else False

				self.state = 'Boiling' if data[1] == '0x53' else 'Waiting'
				self.state = 'Brewing' if data[1] == '0x51' else self.state
				self.state = 'Done' if data[1] in ['0x45','0x47'] else self.state
				self.state = 'No Carafe' if not self.carafe else self.state

				self.waterLevelMessage = data[2]
				self.water_level = self.water_level_number[data[2]]
				self.wifi_strength = int(data[3],16)
				self.coffee_strength = int(data[4],16)
				self.cups = (int(data[5],16) & 15)

				for callback in self._observers:
					logging.info("Sending changes to observer")
					callback(data)
		elif len(data) == 3:
			response = int(data[1],16)
			print(response)
			if response == 0:
				self.error = None
			elif response == 5:
				self.error = self.responses_text[response]
			print(self.error)


	def set_cups(self, number, whole_packet=True, send=True): #cups value can be between 1 - 12. Syntax for cups is 36xx7e where 36 is value for "set cups" xx is how many and 7e is packet terminator
		cups_hex = ""
		if number <= 12 and number >= 1:
			cups_hex = "%0.2X" % number # convert to hex
		else:
			logging.warning("Coffee cups must be a value between 1 and 12. Setting 1 cup.")
			cups_hex = "01"

		cups_hex = "36" + cups_hex + "7e" if whole_packet else cups_hex
		logging.debug(cups_hex)
		if send:
			self.send_command(cups_hex)
		return cups_hex

	def set_grinder(self, value, whole_packet=True, send=True):
		grinder_hex = ""
		if value == True:
			grinder_hex = "01"
		else:
			grinder_hex = "00"
		grinder_hex = "3c" + grinder_hex + "7e" if whole_packet else grinder_hex
		logging.debug(grinder_hex)
		if send:
			self.send_command(grinder_hex)
		return grinder_hex

	def set_strength(self, strength, whole_packet=True, send=True): # strength value can be between 1 - 3 when send to machine the value vill be converterd to 0 - 2
		strength = strength - 1
		strength_hex = ""
		if strength >= 0 and strength <= 2:
			strength_hex = "%0.2X" % strength # convert to hex
		else:
			logging.warning("Coffee strength must be a value between 1 and 3. Setting strength to 1.")
			strength_hex = "00"
		strength_hex = "35" + strength_hex + "7e" if whole_packet else strength_hex
		logging.debug(strength_hex)
		if send:
			self.send_command(strength_hex)
		return strength_hex

	def start_with_current_settings(self, send=True):
		if send:
			self.send_command("37")
		return "37"

	def hotplate_timer(self, time_mins, whole_packet=True, send=True): #Timevalue is for how long the hot plate will be on before auto turning off. Lowest value is 5 min. Max value is ?
		time_hex = ""
		if time_mins < 5:
			logging.warning("Minimum time is 5 minutes.  Setting timer to 5 minutes.")
			time_hex = "05"
		else:
			time_hex = "%0.2X" % time_mins # convert to hex
		time_hex = "3e" + time_hex + "7e" if whole_packet else time_hex
		logging.debug(time_hex)
		if send:
			self.send_command(time_hex)
		return time_hex

	def start_with_settings(self, cups, strength, hotplate, grinder, send=True):
		command_hex = "33" + self.set_cups(cups, whole_packet=False, send=False) + self.set_strength(strength, whole_packet=False, send=False) + self.hotplate_timer(hotplate, whole_packet=False, send=False) + self.set_grinder(grinder, whole_packet=False, send=False) + "7e"
		logging.debug(command_hex)
		if send:
			self.send_command(command_hex)
		return command_hex

	def send_command(self, command):
		opened_connection = False
		if not self._connected:
			self._device.connect((self._ip, self._port))
			self._connected = True
			opened_connection = True
		logging.debug(bytes.fromhex(command))
		self._device.send(bytes.fromhex(command))

		running_time = time.time()
		while True and running_time + 5 > time.time():
			data = self._device.recv(4096) # buffer size is 1024 bytes
			hex_data = list(map(hex, data))
			self.process_command(hex_data)
			logging.debug("Hex Data: {}".format(hex_data)

		if opened_connection:
			self._device.shutdown(socket.SHUT_RDWR)
			self._device.close()
			self._connected = False
