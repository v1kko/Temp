import os
import socket
import select
from multiprocessing import Process
from config import *
"""
This is the main function.
It reads its input from config.py
It also has the ability to stop other processes and restart them might they fail
"""

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((MAIN_HOST, MAIN_PORT))
serversocket.listen(len(modules))

for module, dest in modules.iteritems():
	name, port, host, user, pwd, args = dest

	#For now, only load localhost modules
	#TODO: add remote capability
	if host != 'localhost':
		continue
	
	child = Process(target=module, args=args)
	child.start()

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
	name = clientsocket.recv(100)
	socketlist[name] = clientsocket

#Send start to every module
for x in socketlist.itervalues():
	x.send('START')
