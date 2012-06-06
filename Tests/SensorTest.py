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

def receive(no_block=False):
    return "SRC", "FAIL ODOMETRY 4.6 3.5 2.3"
    

def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class TestSensorsRightInput(unittest.TestCase):
    
    def testMinimumNumberReturnValues(self):
        """ Checking the minimum number of expected values received """
        src, rcv = receive()
        rcv = rcv.split(" ")
        self.assertTrue(len(rcv) >= 3)
    
    def testProperSensorType(self):
        """ Checking wether the second value indicates a proper sensor type """
        sensors = ['LASER', 'ODOMETRY', 'SONAR']
        src, rcv = receive()
        rcv = rcv.split(" ")
        self.assertTrue(rcv[1] in sensors)

    def testReturnValueNumber(self):
        """ Checking the expected number of values """
        src, rcv = receive()
        rcv = rcv.split(" ")
        sensType = rcv[1]
        
        if sensType == 'LASER':
            # TODO: insert right number of parameters
            self.assertEqual(5, len(rcv))
        elif sensType ==  'ODOMETRY':
            self.assertEqual(5, len(rcv))
        elif sensType == 'SONAR':
            # TODO: insert right number of parameters
            self.assertEqual(5, len(rcv))
            
    def testProperSensorParameters(self):
        """ Checking per sensor type for the right amount of parameters """
        src, rcv = receive()
        rcv = rcv.split(" ")
        sensType = rcv[1]
        
        if sensType == 'LASER':
            # TODO: insert right number of parameters
            for x in range(2, len(rcv)):  
                self.assertTrue(isFloat(rcv[x]))
        elif sensType ==  'ODOMETRY':
            for x in range(2, len(rcv)):  
                self.assertTrue(isFloat(rcv[x]))
        elif sensType == 'SONAR':
            # TODO: insert right number of parameters
            for x in range(2, len(rcv)):  
                self.assertTrue(isFloat(rcv[x]))

class TestSensorsWrongInput(unittest.TestCase):
    
    def testReturnValueNumber(self):
        """ Checking the expected number of values """
        src, rcv = receive()
        rcv = rcv.split(" ")
        self.assertEqual(2, len(rcv))
    
    def testWrongInput(self):
        self.assertTrue(False)

if __name__ == "__main__":  
    unittest.main()  