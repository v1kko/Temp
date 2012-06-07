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
    
    def __init__(self):
        self.ctrl = Control(self.__class__.__name__)
        self.TRESHOLD = 0.250
        self.RECOVERTIME = 5
        self.running = True
        self.run()
        
    def run(self):
        while self.running:
            self.check("LASER")
            self.check("SONAR")
    
    def check(self, sensor):
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
        
        for it in vals:
            if it < self.TRESHOLD:
                send("Steering", "ALERT")
                send("Logic", "ALERT")
                sleep(self.RECOVERTIME)
                continue