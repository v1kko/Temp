
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
	mysock  = socket.socket(socket.AF_INET, socket, SOCK_STREAM)
	sockdict = {}
	
#	for x in modules.iterkeys()[MODULE_NAME:]:
