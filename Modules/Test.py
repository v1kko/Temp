# -*- coding: utf-8 -*-
"""
Created on Tue Jun 05 15:38:11 2012

@author: Timothy

This script tests the proper output of the sensor module.
Tests are well defined by their names.

"""
import unittest
import socket
from Control import *

"""
def receive(boolean=True):
    if boolean is True:
        return "SRC", "Steering ODOMETRY 0.3 0.4 0.6"
    else:
        return "SRC", "Sensors ODOMETRY FAIL"
"""



def isFloatAndPositive(num):
    try:
        float(num)
        if float > 0:
            return True
        else:
            return False
    except ValueError:
        return False
        
class Test():
    def __init__(self):
        #Control.init()
        global ctrl
        ctrl = Control(self.__class__.__name__)
        unittest.main(verbosity=2)

class TestSensorsRightInput(unittest.TestCase):

    
    def testProperSensorType(self):
        """ Checking wether the second value indicates a proper sensor type """
        for i, sensType in enumerate(("ODOMETRY", "ODOMETRY", "ODOMETRY")):
            ctrl.send("Sensors", "STEER GET " + sensType)
            src, rcv = ctrl.receive()
            rcv = rcv.split(" ")
            self.assertEqual(sensType, rcv[1])

    def testReturnValueNumber(self):
        """ Checking the expected number of values """
        for i, sensType in enumerate(("ODOMETRY", "ODOMETRY", "ODOMETRY")):
            ctrl.send("Sensors", "STEER GET " + sensType)
            src, rcv = ctrl.receive()
            rcv = rcv.split(" ")
            
            if sensType == 'LASER':
                self.assertEqual(183, len(rcv))
            elif sensType ==  'ODOMETRY':
                self.assertEqual(5, len(rcv))
            elif sensType == 'SONAR':
                self.assertEqual(10, len(rcv))
            
    def testProperSensorParameters(self):
        """ Checking per sensor type for the right amount of parameters """
        for i, sensType in enumerate(("ODOMETRY", "ODOMETRY", "ODOMETRY")):
            ctrl.send("Sensors", "STEER GET " + sensType)
            src, rcv = ctrl.receive()
            rcv = rcv.split(" ")

            if sensType == 'LASER':
                for x in range(2, len(rcv)):  
                    self.assertTrue(isFloatAndPositive(rcv[x]))
            elif sensType ==  'ODOMETRY':
                for x in range(2, len(rcv)):  
                    self.assertTrue(isFloatAndPositive(rcv[x]))
            elif sensType == 'SONAR':
                for x in range(2, len(rcv)):  
                    self.assertTrue(isFloatAndPositive(rcv[x]))

class TestSensorsWrongInput(unittest.TestCase):
    # TODO remove False from receivce paramter
    def testUnkownSensorType(self):
        """ Checking the expected number of values """
        ctrl.send("Sensors", "STEER GET GPS")
        src, rcv = ctrl.receive()
        rcv = rcv.split(" ")
        self.assertEqual(3, len(rcv))
        
    def testNoSensorType(self):
        """ Checking the expected number of values """
        ctrl.send("Sensors", "STEER ")
        src, rcv = ctrl.receive()
        rcv = rcv.split(" ")
        self.assertEqual(3, len(rcv))

    def testTooManyArguments(self):
        """ Checking the expected number of values """
        ctrl.send("Sensors", "STEER GET GPS PLUS MORE ARGUMENTS")
        src, rcv = ctrl.receive()
        rcv = rcv.split(" ")
        self.assertEqual(3, len(rcv))
 
        
S = Test()