import os
import socket
import select
from config import *
"""
This is the main function.
It reads its input from config.py
It also has the ability to stop other processes and restart them might they fail
"""
MODULE_NAME = "" 
MODULE_PORT = ""
MODULE_HOST = ""

Nmodules = len(modules)

for x in modules.iterkeys():
	exec("from Modules." + x + " import *")

for x in modules.iteritems():
	name, dest = x
	port, host, user, pwd, args = dest

	MODULE_NAME = name
	MODULE_PORT = port
	MODULE_HOST = host

	#For now, only load localhost modules
	#TODO: add remote capability
	if host != 'localhost':
		continue
	
	pid = os.fork()

	if pid == 0:
		execstr = name + "("
		for x in args:
			execstr = execstr + str(x)
			execstr = execstr + "," 
		execstr = execstr + ")"
		exec(execstr)
		
	
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((MAIN_HOST, MAIN_PORT))
serversocket.listen(Nmodules)

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
