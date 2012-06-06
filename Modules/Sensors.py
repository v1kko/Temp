# -*- coding: utf-8 -*-
"""
Sensors.py

Purely receiving so far, not finished by any means
"""

from control import *

class Sensors():
    def __init__(self):
        self.data = ""
        
        self.sensors = {"LASER" : "",    # "SENS LASER"
                        "ODOMETRY" : "", # "SENS ODOMETRY <float x> <float y> <float z>"
                        "SONAR" : ""}    # "SENS SONAR <float F1> <float F2> <float F3> <float F4> <float F5> <float F6> <float F7> <float F8>"  
        
        self.running = True
        self.receive()
        
    def receive(self):
        while(self.running):
            src, rcv = receive(True)
            
            # Mine data from Bot stream
            if src == "Interface":
                self.data = self.data + recv

                self.data = self.data.split('\r\n')

                # TODO: Refactor msges
                for i in range(len(data) - 1):
                    if not self.data[i].find("Scanner1"):
                        string = "LASER"
                        self.sensors["LASER"] = string.split(' ')[12].replace(',', ' ')
                        break
                    elif not self.data[i].find("Odometry"):
                        temp = self.data[i].split(' ')
                        vals = temp[6].split(',')
                        self.sensors["ODOMETRY"] = "ODOMETRY " + vals[0] + vals[1] + vals[2].split('}')[0]
                        break
                    elif not self.data[i].find("Sonar"):
                        temp = self.data[i].split(' ')
                        string = "SONAR"
                        # XXX: Not sure if OK
                        for i in range(8):
                            string = string + ' ' +  temp[5 * i + 8].split('}')[0]
                        
                        self.sensors["SONAR"] = sonar[i]
                        
                self.data = self.data[len(data) - 1]
            
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
                if rcv[0] == GET:
                    # XXX: if x in y instead of try?
                    try:
                        send(src + ' ' + self.sensors[rcv[1]] )
                    except:
                        send(src + ' ' + rcv[1] + ' FAIL' )

    # Well obviously...
    def reset(self):
        self.data = ""
        for i in self.sensors.keys():
            self.sensors[i] = ""
            
        self.running = True
        self.receive()