# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 11:50:38 2012

@author: arjen

Reads sensor (sonar/laser) data & checks whether obstacle distance is <
given treshold, and sends an alarm msg if so.

TODO: Check msg source?
"""

from Control import *

class Alert:
    
    #Initialises control class, and tresholds
    def __init__(self):
        self.ctrl = Control(self.__class__.__name__)
        self.TRESHOLD_S = 0.4
        self.TRESHOLD_L = 0.25
        self.RECOVERTIME = 3
        self.running = True
        self.run()
        
    # Alternate between checkin Laser and Sonar distance
    def run(self):
        while self.running:
            self.check("LASER", self.TRESHOLD_L)
            self.check("SONAR", self.TRESHOLD_S)
    
    # Get sensor values, compare each to treshold, send out ALERT if below
    def check(self, sensor, treshold):
        data = ""
        self.ctrl.send("Sensors", "GET " + sensor)
        while not data[:5] == sensor:
            data = self.ctrl.receive()
            if data == None:
                break
            else:
                src, data = data
                
            if src == "main" and data == "STOP":
                self.running = False
                exit()
                
        vals = data[6:].split(' ')
        
        # Send out alert & sleep when on collision course
        for it in vals:
            if it < treshold:
                send("Steering", "ALERT")
                send("Logic", "ALERT")
                sleep(self.RECOVERTIME)
                continue