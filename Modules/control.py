def receive (no_block=False):
	"""
	This is the receive function implemented in every Module to communicate
	with other modules
	Returns the source and data
	Returns None when no_block = true but no data is received
	"""
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
