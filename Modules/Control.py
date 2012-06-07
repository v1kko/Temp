import socket
from select import select
from Queue import Queue

class Control: 
	"""
	This class must be in the __init__ function of all modules for them to
	work correctly and be able to use send & receive
	"""
	def receive (self, no_block=False):
		"""
		This is the receive function implemented in every Module to communicate
		with other modules
		Returns the source and data
		Returns None when no_block = true but no data is received
		"""
		while True:
			for name, sock in self.sockdict.iteritems():
				ready, _, _ = select([sock], [], [], 0.05)
				for x in ready:
					self.msgqueue.put((name, x.recv(1024)))
			if self.msgqueue.empty() and no_block:
				return None

		src, data = self.msgqueue.get()
		if src == 'Test':
			self.DEBUG = True
			src, _, data = data.partition(" ")

		return src, data

	def send (self, dest, data):
		"""
		This is the send function implemented in every module to communicate
		with other modules
		Needs the destination and data to send
		Returns False on error
		Returns True on succes
		"""
		try:
			sock = self.sockdict[dest]
		except KeyError:
			return False

		sock.send(data)
		if self.DEBUG == True:
			sock = self.sockdict['Test']
			sock.send(data)

		return True

	def __init__(self, mname):
		from config import modules, MAIN_PORT, MAIN_HOST

		self.DEBUG = False
		self.sockdict = {}
		self.msgqueue = Queue()
		#Find the right name and information of the module
		for name, port, host, user, pwd, args in modules.itervalues():
			if name == mname:
				self.MODULE_HOST = host
				self.MODULE_PORT = port
				self.MODULE_NAME = name
			else:
				self.sockdict[name] = ''
		self.mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.mysock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.mysock.bind((self.MODULE_HOST, self.MODULE_PORT))
		self.mysock.listen(len(modules))

		#Send & get OK from main
		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		clientsocket.connect((MAIN_HOST, MAIN_PORT))
		clientsocket.send(self.MODULE_NAME)
		self.sockdict['main'] = clientsocket
		while clientsocket.recv(1024) != 'START':
			pass

		#connect to the modules you should connect to
		for name, port, host, user, pwd, args in modules.itervalues():
			if name == self.MODULE_NAME:
				break
			clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clientsocket.connect((host, port))
			clientsocket.send(self.MODULE_NAME)
			self.sockdict[name] = clientsocket
			
		#Wait for response of every module
		while True: 
			for x in self.sockdict.itervalues():
				if x == '':
					break;
			else:
				break
			clientsocket, _ = self.mysock.accept()
			name = clientsocket.recv(100)
			self.sockdict[name] = clientsocket
