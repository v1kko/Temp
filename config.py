from Modules.Sensors import *
from Modules.Steering import *

modules = {
#Format = Module : (modulename, port, host, login, password, (arguments))
#Example:
	#module:(modulename, 1000, 'deze', 'vikko', 'vokko', (run, gridsize))
	Steering:('Steering', 5432, 'localhost', '', '', (1, 1)),
	Sensors:('Sensors', 54332, 'localhost', '', '',()),
}


MAIN_PORT = 12341
MAIN_HOST = 'localhost'
INTERFACE_PORT = 3000
