"""
This is a skeleton for a Module in our system
Please remove these lines if you use it
"""
from Control import *
from time import *
class Interface:
    def __init__(self, robothost, robotport):
        self.ctr = Control(self.__class__.__name__)
        self.robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.robot.connect((robothost, robotport))
            except socket.error:
                print "NO CONNECTION TO THE ROBOT, WTF ARE YOU DOING!"
                sleep(5)
                continue
            break
        self.mainloop()
        exit(0)


    def mainloop(self):
        #Spawn Bro-bot
        self.robot.send(ROBOT_COMMAND)
        while True:
            recv = self.ctr.receive(True)
            if recv:
                src, data = recv
                if src == 'main' and data == 'STOP':
                    break
                self.robot.send(data)
            
            ready, _, _ = select(list(self.robot),(),(), 0.05)
            for x in ready:
                data = x.recv(1024)
                self.ctr.send('Sensors', data)
