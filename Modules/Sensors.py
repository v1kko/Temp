# -*- coding: utf-8 -*-
"""
Sensors.py

TODO: Comments
"""

from Control import *

class Sensors:
    def __init__(self):
        self.ctrl = Control(self.__class__.__name__)
        self.data = ""
        
        self.sensors = {"LASER" : "",    # "SENS LASER"
                        "ODOMETRY" : "", # "SENS ODOMETRY <float x> <float y> <float z>"
                        "SONAR" : ""}    # "SENS SONAR <float F1> <float F2> <float F3> <float F4> <float F5> <float F6> <float F7> <float F8>"  
        
        self.running = True
        self.receive()
        
    def receive(self):
        while(self.running):
            src, rcv = self.ctrl.receive(True)
            
            # Mine data from Bot stream
            if src == "Interface":
                self.data = self.data + rcv

                self.data = self.data.split('\r\n')

                for i in range(len(self.data) - 1):
                    # LASER
                    if not self.data[i].find("Scanner1"):
                        self.sensors["LASER"] = "LASER " + self.data[i].split(' ')[12].replace(',', ' ')

                    # ODOMETER
                    elif not self.data[i].find("Odometry"):
                        temp = self.data[i].split(' ')
                        vals = temp[6].split(',')
                        self.sensors["ODOMETRY"] = "ODOMETRY " + vals[0] + vals[1] + vals[2].split('}')[0]

                    # SONAR
                    elif not self.data[i].find("Sonar"):
                        temp = self.data[i].split(' ')
                        string = "SONAR"
                        # XXX: Not sure if OK
                        for i in range(8):
                            val = temp[5 * i + 8].split('}')[0]
                            string = string + ' ' + val
                        self.sensors["SONAR"] = string
                        
                self.data = self.data[len(self.data) - 1]
            
            # Respond to msges from main
            # TODO: respond to resets n stuff
            elif src == "Main":
                # 
                if rcv == "RESTART":
                    self.running = False
                    self.reset()
                if rcv == "STOP":
                    self.running = False

            # Reply to GET
            else:
                rcv = rcv.split(' ')
                if rcv[0] == "GET":
                    # XXX: if x in y instead of try?
                    try:
                        self.ctrl.send(src + ' ' + self.sensors[rcv[1]] )
                    except:
                        self.ctrl.send(src + ' ' + rcv[1] + " FAIL" )

    # Well obviously...
    def reset(self):
        self.data = ""
        for i in self.sensors.keys():
            self.sensors[i] = ""
            
        self.running = True
        self.receive()
