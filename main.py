import os
from config import *

MODULE_NAME = "" 
MODULE_PORT = ""
MODULE_HOST = ""

for x in modules.iterkeys():
	exec("import  Modules." + x)

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
		
	 


