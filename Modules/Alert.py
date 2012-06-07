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
        init()
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
        self.send("Sensors", "GET " + sensor)
        while not data[:5] == sensor:
            src, data = receive()
            
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