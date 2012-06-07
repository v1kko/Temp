"""
    Simple Script to analyse sensor information from different angles

    USAGE:
        - press 'g' to spawn the P2DX robot
        - press 'w', 's', 'a', 'd' to respectively:
             move forward,
             move backwards,
             turn left,
             turn right
        - press 'o', 'l' to increase resp. decrease the robots speed
        - press 'f' to flush the received data
              (do this before you asking information
        - press 'h', 'j', 'k' to respectively:
             print Sonar data
             print Laser data
             print Odometry data
            

"""

import socket
import Tkinter as tk

# connect to the UT engine
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 3000))

class Besturing():
    s = None
    speed = 1.0
    spawned = False

    def spawnRobot(self):
    
        if self.spawned is False:
            print 'Spawning robot...'
            s.send('INIT {ClassName USARBot.P2DX} {Location 4.5,1.8,1.9}' +
                   '{Name Strike}\r\n')
            self.spawned = True
        else:
            print 'Robot already spawned...'

    def turnLeft(self):
        print 'Turning Left...'
        s.send('DRIVE {Left -1.0} {Right 1.0}\r\n')

    def turnRight(self):
        print 'Turning right...'
        s.send('DRIVE {Left 1.0} {Right -1.0}\r\n')

    def moveForward(self):
        print 'Driving forward...'
        s.send('DRIVE {Left ' + str(self.speed) + '} {Right ' +
               str(self.speed) + '}\r\n')

    def moveBackwards(self):
        print 'Driving backwards...'
        s.send('DRIVE {Left -' + str(self.speed) + '} {Right -' +
               str(self.speed) + '}\r\n')

    def stopMoving(self):
        print 'Stopped moving...'
        s.send('DRIVE {Left 0.0} {Right 0.0}\r\n')
        
    def getSensorInfoSonar(self):
        print 'Sonar sensor info...'
        d = s.recv(4096)
        ind = d.find("Type Sonar") - 1
        ind2 = d[ind:].find("F8") + ind
        ind3 = d[ind2:].find("}") + ind2
        print d[ind:ind3] + "\n" 

    def getSensorInfoLaser(self):
        print 'Laser sensor info...'
        d = s.recv(4096)
        ind = d.find("Type RangeScanner") - 1
        ind2 = d[ind:].find("SEN") + ind - 2
        print d[ind:ind2] + "\n" 

    def getSensorInfoOdometry(self):
        print 'Odometry sensor info...'
        d = s.recv(4096)
        ind = d.find("Type Odometry") - 1
        ind2 = d[ind:].find("SEN") + ind - 2
        print d[ind:ind2] + "\n" 

    def flushData(self):
        d = s.recv(2048)
        while len(d) == 2048:
            d = s.recv(2048)

    def handleKeypress(self, event):
        pressedKey = event.char
        
        if pressedKey == 'w':
            self.moveForward()
        elif pressedKey == 's':
            self.moveBackwards()
        elif pressedKey == 'a':
            self.turnLeft()
        elif pressedKey == 'd':
            self.turnRight()
        elif pressedKey == 'g':
            self.spawnRobot()
        elif pressedKey == 'x':
            self.stopMoving()
        elif pressedKey == 'o':
            print "Increased speed by one..."
            self.speed = self.speed + 1.0
        elif pressedKey == 'l':
            print "Lowered speed by one..."
            self.speed = self.speed - 1.0
        elif pressedKey == 'h':
            self.getSensorInfoSonar()
        elif pressedKey == 'j':
            self.getSensorInfoLaser()
        elif pressedKey == 'k':
            self.getSensorInfoOdometry()
        elif pressedKey == 'f':
            self.flushData()
        else:
            print ".. unkown key .."

    def printManual(self):
        print "||    MOVE:       w-s-a-d   ||",
        print "||    SONAR:      h         ||"
        print "||    SPEED INCR: o         ||",
        print "||    LASER:      j         ||"
        print "||    SPEED DECR: p         ||",
        print "||    ODOMETRY:   k         ||"
        print "\n... you may start ..."

    def __init__(self, s):
        self.s = s
        mainHandle = tk.Tk()
        mainHandle.bind_all('<Key>', self.handleKeypress)
        mainHandle.withdraw()
        self.printManual()
        mainHandle.mainloop()

b = Besturing(s)


