"""
This is a skeleton for a Module in our system
Please remove these lines if you use it
"""
from Control import *

class Skeleton:
    def __init__(self, robotport, robothost):
        ctr = Control(self.__class__.__name__)
		self.robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.robot.connect((self.robothost, self.robotport))
        mainloop()
        exit(0)


    def mainloop:
        while True:
            recv = ctr.receive(True)
            if recv:
                src, data = recv
                if src = 'main' and data == 'STOP':
                    break
                robot.send(data)
            
            ready, _, _ = select(list(robot),(),(), 0.05)
            
            for x in ready:
                data = x.recv(1024)
                ctr.send('Sensors', data)
                
