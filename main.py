import os
import socket
import select
from config import *

MODULE_NAME = "" 
MODULE_PORT = ""
MODULE_HOST = ""
MAIN_PORT = 12341
MAIN_HOST = 'localhost'

Nmodules = len(modules)

for x in modules.iterkeys():
	exec("from Modules." + x + " import *")

for x in modules.iteritems():
	name, dest = x
	port, host, user, pwd = dest

	MODULE_NAME = name
	MODULE_PORT = port
	MODULE_HOST = host

#For now, only load localhost modules
#TODO: add remote capability
	if host != 'localhost':
		continue
	
	pid = os.fork()

	if pid == 0:
		#exec(name + "()")
		exit()
	
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((MAIN_HOST, MAIN_PORT))

serversocket.listen(5)

socketlist = {}
for x in modules.iterkeys():
	socketlist[x] = ''

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

#Send start to every module
for x in socketlist.itervalues():
	x.send('START')
