# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 14:42:23 2012

@author: arjen

Drives around the bot aimlessly and randomly, trying not to hit any obstacles.
This is the extremely simple version which only looks forward and does not take
notice of the mounting angles of the middle two sonar sensors.

Uses only laser & sonar
"""

import random
import Control

class Driverandom:
    
    def __init__(self):
        self.ctrl = Control(self.__class__.__name__)
        self.gridSize = 1.0
        self.treshold_l = 0.4
        self.treshold_s = 0.25
        self.sonar = ""
        self.laser = ""
        self.running = True
        self.drive(0)
    
    # Retrieves sensor data from the sensor module
    def getData(self, sensor):
        self.ctrl.send("Sensors", "GET " + sensor)
        data = None
        while data == None or data[0] != "Sensors" or (data[0] == "Sensors" and data[1][:5] != sensor):
            data = self.ctrl.receive()

            if data != None:
                src, data = data
            if src == "main" and data == "STOP":
                self.running = False
                exit()
        return data[6:].split(' ')

    def getGridSize(self):
        return 1.0
    
    # Returns a random amount of grid steps to take, from within a collision
    # free range
    def getSteps(self, dist):
        # XXX If stupid just floor() (or int())
        dist_norm = ceil(dist) if (dist % floor(dist)) > 0.9 else floor(dist)
        return random.randrange(1, dist_norm)

    #Drives a random path, based on a given seed
    def drive(self, seed):
        random.seed(seed)
        while(self.running):
            self.getGridSize()
            
            turn_deg = random.randrange(0,4,1)
            self.ctrl.send("Steering", "turn 1 " + str(turn_deg * 90))
            
            self.sonar = self.getData("SONAR")
            self.laser = self.getData("LASER")
            
            # TODO: Laser more accurate
            # Get current sensor data
            laserFrontDistance = float(self.laser[90]) - self.treshold_l
            sonarFrontDistance = (float(self.sonar[3]) + float(self.sonar[4]))/2 - self.treshold_s
            
            # The 1.5 is arbitrary, need to experiment for perfect value (if it
            # exists)
            if laserFrontDistance - sonarFrontDistance > 1.5:
                steps = self.getSteps(sonarFrontDistance)
            elif sonarFrontDistance - laserFrontDistance > 1.5:
                steps = self.getSteps(laserFrontDistance)
            else:
                steps = self.getSteps((laserFrontDistance + sonarFrontDistance) / 2)
            
            self.ctrl.send("Steering", "Move 1 " + steps / self.gridSize)