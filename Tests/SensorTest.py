# -*- coding: utf-8 -*-
"""
Created on Tue Jun 05 15:38:11 2012

@author: Timothy
"""
import unittest
import socket
import sys

#sys.path.append('../Modules')
#from Control import *
#import Sensors

def receive(boolean=True):
    if boolean is True:
        return "SRC", "ODOMETRY 0.3 0.4 0.2"
    else:
        return "SRC", "ODOMETRY FAIL"

def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class TestSensorsRightInput(unittest.TestCase):
    
    def testProperSensorType(self):
        """ Checking wether the second value indicates a proper sensor type """
        for i, sensType in enumerate(("ODOMETRY", "ODOMETRY", "ODOMETRY")):
            src, rcv = receive()
            rcv = rcv.split(" ")
            self.assertEqual(sensType, rcv[0])

    def testReturnValueNumber(self):
        """ Checking the expected number of values """
        for i, sensType in enumerate(("ODOMETRY", "ODOMETRY", "ODOMETRY")):
            src, rcv = receive()
            rcv = rcv.split(" ")
            
            if sensType == 'LASER':
                self.assertEqual(181, len(rcv))
            elif sensType ==  'ODOMETRY':
                self.assertEqual(4, len(rcv))
            elif sensType == 'SONAR':
                self.assertEqual(9, len(rcv))
            
    def testProperSensorParameters(self):
        """ Checking per sensor type for the right amount of parameters """
        for i, sensType in enumerate(("ODOMETRY", "ODOMETRY", "ODOMETRY")):
            src, rcv = receive()
            rcv = rcv.split(" ")

            if sensType == 'LASER':
                for x in range(1, len(rcv)):  
                    self.assertTrue(isFloat(rcv[x]))
            elif sensType ==  'ODOMETRY':
                for x in range(1, len(rcv)):  
                    self.assertTrue(isFloat(rcv[x]))
            elif sensType == 'SONAR':
                for x in range(1, len(rcv)):  
                    self.assertTrue(isFloat(rcv[x]))

class TestSensorsWrongInput(unittest.TestCase):
    
    def testReturnValueNumber(self):
        """ Checking the expected number of values """
        #send("SENS", "GPS")
        src, rcv = receive(False)
        rcv = rcv.split(" ")
        self.assertEqual(2, len(rcv))
    
if __name__ == "__main__": 
    unittest.main()