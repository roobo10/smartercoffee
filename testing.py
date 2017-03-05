import logging
import smartercoffee
import sys
from colorama import Fore, Back, Style, init

def update(data):
	global s
	n = 12
	m = n -1
	logging.debug("Settings updated.")
	print("┌" + "".ljust(n,"─") + "┬" + "".ljust(n,"─") +"┐")
	print("│"+"State".ljust(n) +"│ "+ s.state.ljust(m)+"│")
	print("├" + "".ljust(n,"─") + "┼" + "".ljust(n,"─") +"┤")
	print("│"+"Hotplate".ljust(n) +"│ "+ ("ON" if s.hotplate else "Off").ljust(m)+"│")
	print("├" + "".ljust(n,"─") + "┼" + "".ljust(n,"─") +"┤")
	print("│"+"Grinder".ljust(n) + "│ "+("Grinder" if s.grinder else "Filter").ljust(m)+"│")
	print("├" + "".ljust(n,"─") + "┼" + "".ljust(n,"─") +"┤")
	print("│"+"Carafe".ljust(n) + "│ "+("Present" if s.carafe else "NO CARAFE").ljust(m)+"│")
	print("├" + "".ljust(n,"─") + "┼" + "".ljust(n,"─") +"┤")
	print("│"+"Water Level".ljust(n) +"│ "+ s.water_level_text[s.water_level].ljust(m)+"│")
	print("├" + "".ljust(n,"─") + "┼" + "".ljust(n,"─") +"┤")
	print("│"+"Cups".ljust(n) +"│ "+ str(s.cups).ljust(m)+"│")
	print("├" + "".ljust(n,"─") + "┼" + "".ljust(n,"─") +"┤")
	print("│"+"Strength".ljust(n) +"│ "+ s.coffee_strength_text[s.coffee_strength].ljust(m)+"│")
	print("└" + "".ljust(n,"─") + "┴" + "".ljust(n,"─") +"┘")


levels = ['debug','info','warning','error','critical']

log_level = 'critical'

if len(sys.argv) == 2:
    log_level = sys.argv[1] if sys.argv[1] in levels else 'critical'

print("Logging level: "+Fore.RED+log_level.upper()+ "."+Fore.WHITE)

numeric_level = getattr(logging, log_level.upper(), 0)

if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % log_level)

logging.basicConfig(level=numeric_level)


s = smartercoffee.SmarterCoffee('192.168.1.55')
s.start_server()
s.watch_updates(update)

last_command = ""
while True:
	p = input(">>")
	if p == ".exit":
		exit
	elif p == ".status":
		print(s.grinder)
		print(s.carafe)
		print(s.hotplate)
	elif p[:8] == ".grinder":
		if p[-2:].strip() == "on":
			last_command = s.set_grinder(True)
		else:
			last_command = s.set_grinder(False)
	elif p[:9] == ".strength":
		last_command = s.set_strength(int(p[10]))
	elif p[:5] == ".cups":
		last_command = s.set_cups(int(p[6]))
	elif p == ".make":
		logging.debug("Make with Current Settings...")
		s.start_with_current_settings()
	elif p[:6] == ".make ":
		s.start_with_settings(1,2,5,False)
	elif p == ".send":
		s.send_command(last_command)
