'''
@since: 04 Jun 2012
@author: Cedric Blom
@version: 1.0

@summary: 
'''

from Queue import Queue
from re import match
import math
import Control



class Steering:
    def __init__(self):
        Control.init()
        self.stop_signal = False
        self.__command_queue = Queue()
        self.__active_task = ''
        self.__FUNCS = {'SET' : (self.add, str, float),
                        'MOVE' : (self.move, float, float),
                        'TURN' : (self.turn, float, float)}
        self.receive()


    def receive(self):
        while not self.stop_signal:
            recv = Control.receive()
            if recv == None:
                continue
            self.__active_task, data = map(str.upper, recv)
            if self.__hard_signal(data):
                continue
            else:
                self.__command_queue.put(recv)

            self.__active_task, data = map(str.upper, self.__command_queue.get())
            if match('^FAIL\ $', data):
                #TODO: Error handling
                pass
            elif not match('^(MOVE|TURN\ [0-9]+(\.[0-9]+)?|\.[0-9]+)|' + \
                           '(SET\ MOVE|TURN)\ [0-9]+(\.[0-9]+)?|\.[0-9]+$', data):
                Control.send(self.__active_task, 'FAIL Unknown message format')
            else:
                func, parm1, parm2 = data.split()
                load, cast1, cast2 = self.__FUNCS[func]
                load(cast1(parm1), cast2(parm2))


    def __hard_signal(self, data):
        if data == 'ALARM':
            self.__flush()
            Control.send(self.__active_task, 'FAIL Alarm signal received')
            return True
        elif data == 'STOP':
            self.stop_signal = True
            return True
        return False


    def add(self, set_type, step_size):
        if set_type.upper() == 'MOVE':
            self.step_dist = step_size
        elif set_type.upper() == 'TURN':
            self.step_angle = step_size


    def move(self, speed, distance):    
        start = True
        while True:
            odo = self.__odometry()
            if not odo:
                ins = 'DRIVE {Left %f} {Right %f}\r\n' % (0.0, 0.0)
                Control.send('Interface', ins)
                Control.send(self.__active_task, 'FAIL Robot movement aborted')
                return

            if start:
                xs, ys = odo[0:2]
                ins = 'DRIVE {Left %f} {Right %f}\r\n' % (speed, speed)
                Control.send('Interface', ins)
                start = False

            xa, ya = odo[0:2]
            xr = xa - xs
            yr = ya - ys
            if math.sqrt(xr*xr + yr*yr) >= distance:
                ins = 'DRIVE {Left %f} {Right %f}\r\n' % (0.0, 0.0)
                Control.send('Interface', ins)
                Control.send(self.__active_task, 'OK')
                return


    def turn(self, speed, angle):
        start = True
        rad = angle / 180.0 * math.pi
        while True:
            odo = self.__odometry()
            if not odo:
                ins = 'DRIVE {Left %f} {Right %f}\r\n' % (0.0, 0.0)
                Control.send('Interface', ins)
                Control.send(self.__active_task, 'FAIL Robot movement aborted')
                return

            if start:
                ts = odo[3]
                if angle < 0.0:
                    drive = (-speed, speed)
                else:
                    drive = (speed, -speed)
                ins = 'DRIVE {Left %f} {Right %f}\r\n' % drive
                Control.send('Interface', ins)
                start = False

            ta = odo[3]
            tr = ta - ts
            if abs(tr) >= rad:
                ins = 'DRIVE {Left %f} {Right %f}\r\n' % (0.0, 0.0)
                Control.send('Interface', ins)
                Control.send(self.__active_task, 'OK')
                return


    def __flush(self):
        while not self.__command_queue.empty():
            self.__command_queue.get()


    def __odometry(self):
        if not Control.send('Sensors', 'GET ODOMETRY'):
            return
        
        while True:
            recv = Control.receive(True)
            if not recv:
                Control.send('Control', 'FAIL Expecting message from sensors')
                return
            
            module, data = map(str.upper, recv)
            if self.__hard_signal(data):
                return
            if module == 'SENSORS' and match('^ODOMETRY\ ' + \
                '([0-9]+(\.[0-9]+)?|\.[0-9]+\ ){2}' + \
                '[0-9]+(\.[0-9]+)?|\.[0-9]+$', data):
                return map(float, data.split(None)[1:4])
            else:
                if self.__command_queue.full():
                    if not Control.send(self.__active_task, 'FAIL Queue is full'):
                        return
                else:
                    self.__command_queue.put(recv)
