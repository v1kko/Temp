# -*- coding: utf-8 -*-
"""
Sensors.py

Purely receiving so far, not finished by any means
"""

from control import *

class Sensors():
    def __init__(self):
        self.data = ""
        
        self.sensors = {"LASER" : "",  #"SENS LASER"
                        "ODOMETRY" : "", # "SENS ODOMETRY <float x> <float y> <float z>"
                        "SONAR" : ""} #"SENS LASER"  
        
        self.running = True
        self.run()
        
    def run(self):
        while(self.running):
            src, rcv = receive(True)
            
            # Mine data from Bot stream
            if src == "Interface":
                self.data = self.data + recv

                self.data = self.data.split('\r\n')

                # TODO: Refactor msges
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
            
            # Respond to msges from main
            # TODO: respond to resets n stuff
            elif src == "Main":
                if rcv == "RESTART":
                    self.running = False
                    self.reset()

            # Reply to GET
            else:
                rcv = rcv.split(' ')
                if rcv[0] == GET:
                    # XXX: if x in y instead of try?
                    try:
                        send(src + ' SENS ' + recv[1] + ' ' + self.sensors[recv[1]] )
                    except:
                        send(src + ' SENS FAIL ' + recv[1] + ' ' )

    # Well obviously...
    def reset(self):
        self.data = ""
        for i in self.sensors.keys():
            self.sensors[i] = ""
            
        self.running = True
        self.run()