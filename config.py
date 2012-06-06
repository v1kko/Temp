modules = {
#Format = Modulename : (port, host, login, password, (arguments))
#Example:
	#'module':(1000, 'deze', 'vikko', 'vokko', (run, gridsize))
	'Steering':(5432, 'localhost', '', '', (1, 1)),
	'Sensors':(5432, 'localhost', '', '',()),
}

MAIN_PORT = 12341
MAIN_HOST = 'localhost'
INTERFACE_PORT = 3000
