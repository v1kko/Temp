from Modules.Sensors import *
from Modules.Steering import *
from Modules.Interface import *

modules = {
#Format = Module : (modulename, port, host, login, password, (arguments))
#Example:
	#module:(modulename, 1000, 'deze', 'vikko', 'vokko', (run, gridsize))
	Interface:('Interface', 2332, 'localhost', '', '', ('localhost', 3000)),
	Steering:('Steering', 22532, 'localhost', '', '', ()),
	Sensors:('Sensors', 54332, 'localhost', '', '',()),
}


MAIN_PORT = 12341
MAIN_HOST = 'localhost'
INTERFACE_PORT = 3000
