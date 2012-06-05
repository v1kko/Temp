# -*- coding: utf-8 -*-
"""
Sensors.py

Purely receiving so far, not finished by any means
"""

from control import *

class Sensors():
    def __init__(self):
        self.data = ""
        
        self.sensors = {"ODOMETRY" : "",
                        "LASER" : "",
                        "SONAR" : ""}     
        
        self.running = True
        self.run()
        
    def run(self):
        while(self.running):
            src, rcv = receive(True)
            
            if src == "Interface":
                self.data = self.data + recv

                self.data = self.data.split('\r\n')

                for i in range(len(data) - 1):
                    if not data[i].find("Laser"):
                        self.sensors["LASER"] = data[i]
                        break
                    elif not data[i].find("Odometry"):
                        self.sensors["ODOMETRY"] = data[i]
                        break
                    elif not data[i].find("Sonar"):
                        self.sensors["SONAR"] = sonar[i]
                        
                self.data = self.data[len(data) - 1]
            
            else:
                self.data = self.data.split(' ')
                if self.data[0] == GET:
                    try:
                        send(src + ' SENS ' + data[1] + ' ' + self.sensors[data[1]] )
                    except:
                        send(src + ' SENS FAIL ' + data[1] + ' ' )
                        
                        
"SENS ODOMETRY <float x> <float y> <float z>"