from Modules.Sensors import *
from Modules.Steering import *
from Modules.Interface import *
from Modules.Test import *

ROBOT_PORT = 1337
ROBOT_HOST = 'localhost'
ROBOT_COMMAND = "INIT {ClassName USARBot.P2DX} {Location 4.5,1.9,1.8}"
MAIN_PORT = 12341
MAIN_HOST = 'localhost'
INTERFACE_PORT = 3000
GRID_SIZE = 1

modules = {
#Format = Module : (modulename, port, host, login, password, (arguments))
#Example:
	#module:(modulename, 1000, 'deze', 'vikko', 'vokko', (run, gridsize))
	Interface:('Interface', 2332, 'localhost', '', '', (ROBOT_HOST, ROBOT_PORT)),
	Steering:('Steering', 22532, 'localhost', '', '', (GRID_SIZE,)),
	Sensors:('Sensors', 54332, 'localhost', '', '',()),
	Test:('Test', 54232, 'localhost', '', '',()),
}
