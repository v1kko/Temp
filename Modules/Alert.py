# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 11:50:38 2012

@author: arjen
"""

from Control import *

class Alert:
    
    def __init__(self):
        init()
        self.running = True
        self.run()
        
    def run(self):
        while self.running:
            data = ""
            self.send("Sensors", "GET ODOMETRY")
            while not data[0:7] == "ODOMETRY":
                src, data = receive()