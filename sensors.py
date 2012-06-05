# -*- coding: utf-8 -*-
"""
Sensors.py
"""

from control import *

class Sensors():
    def __init__(self):
        self.sock = None        
        
        self.laser = ""
        self.odometer = ""
        self.sonar = ""
        
        self.setup(("localhost", 3000))        
        
        self.running = True
        self.run()
    
    def setup(self, addr):
        self.sock = socket.create_connection(addr)
        
    def run(self):
        while(self.running):
            src, data = receive(True)
            
            if data != None:
                data = data.split('\r\n')

                for i in range(len(data)):
                    if not data[i].find("Laser"):
                        self.laser = data[i]
                    elif not data[i].find("Odometer"):
                        self.odometer = data[i]
                        break
                    elif not data[i].find("Sonar"):
                        self.sonar = sonar[i]