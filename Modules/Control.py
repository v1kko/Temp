
def receive (no_block=False):
	"""
	This is the receive function implemented in every Module to communicate
	with other modules
	Returns the source and data
	Returns None when no_block = true but no data is received
	"""
	if src == 'Test':
		src = "STUB"
	src = "STUB"
	data = "STUB"
	return (src, data)
def send (dest, data):
	"""
	This is the send function implemented in every module to communicate
	with other modules
	Needs the destination and data to send
	Returns False on error
	Returns True on succes
	"""
		
	return
def init ():
	"""
	This function must be in the __init__ function of all modules for them to
	work correctly
	Returns nothing
	"""
	global mysock, sockdict
	mysock = socket.socket(socket.AF_INET, socket, SOCK_STREAM)
	mysock.bind((MODULE_HOST, MODULE_PORT))
	sockdict = {}
	
	for x in modules.iteritems()[:MODULE_NAME]:
		name, dest = x
		port, host, user, pwd, args = dest
		
		if name == MODULE_NAME:
			continue
		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		clientsocket.connect((host, port))
		clientsocket.send(MODULE_NAME)
		sockdict[name] = clientsocket
	
	#Wait for response of every module
	while True: 
		for x in socketlist.itervalues():
			if x == '':
				break;
		else:
			break
			
		clientsocket, _ = serversocket.accept()
		name = clientsocket.recv()
		socketlist[name] = clientsocket
