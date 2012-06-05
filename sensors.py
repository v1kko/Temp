# -*- coding: utf-8 -*-
"""
Sensors.py

Purely receiving so far, not finished by any means
"""

from control import *

class Sensors():
    def __init__(self):
        self.sock = None   
        
        self.data = ""
        
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
            src, rcv = receive(True)
            
            self.data = self.data + recv            
            
            if data != None:
                data = data.split('\r\n')

                for i in range(len(data) - 1):
                    if not data[i].find("Laser"):
                        self.laser = data[i]
                    elif not data[i].find("Odometer"):
                        self.odometer = data[i]
                        break
                    elif not data[i].find("Sonar"):
                        self.sonar = sonar[i]
                        
                self.data = self.data[len(data) - 1]
    