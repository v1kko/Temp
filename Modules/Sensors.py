# -*- coding: utf-8 -*-
"""
Sensors.py

Purely receiving so far, not finished by any means
"""

from Control import *

class Sensors:
    def __init__(self):
        self.data = ""
        
        self.sensors = {"LASER" : "",    # "SENS LASER"
                        "ODOMETRY" : "", # "SENS ODOMETRY <float x> <float y> <float z>"
                        "SONAR" : ""}    # "SENS SONAR <float F1> <float F2> <float F3> <float F4> <float F5> <float F6> <float F7> <float F8>"  
        
        self.running = True
        Control.init()
        self.receive()
        
    def receive(self):
        while(self.running):
            src, rcv = receive(True)
            
            # Mine data from Bot stream
            if src == "Interface":
                self.data = self.data + recv

                self.data = self.data.split('\r\n')

                for i in range(len(data) - 1):
                    # LASER
                    if not self.data[i].find("Scanner1"):
                        vals = self.data[i].split(' ')[12]
                        vals_float = vals.split(',')
                        for float(i) in vals_float:
                            if i < TRESHOLD:
                                send("Steering", "ALERT")
                                send("Logic", "ALERT")
                                break
                        else:
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
                            if float(val) < TRESHOLD:
                                send("Steering", "ALERT")
                                send("Logic", "ALERT")
                                break
                            
                            string = string + ' ' + val
                        
                        else: self.sensors["SONAR"] = string
                        
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
                if rcv[0] == "GET":
                    # XXX: if x in y instead of try?
                    try:
                        send(src + ' ' + self.sensors[rcv[1]] )
                    except:
                        send(src + ' ' + rcv[1] + " FAIL" )

    # Well obviously...
    def reset(self):
        self.data = ""
        for i in self.sensors.keys():
            self.sensors[i] = ""
            
        self.running = True
        self.receive()
