from Queue import Queue
from re import match
import Control
import sys


class Steering:
    def __init__(self, grid_size, angle_size):
        self.grid_size = grid_size
        self.angle_size = angle_size
        self.__command_queue = Queue()
        self.__active_task = ''
        self.__FUNCS = {'SET' : (self.add, str, float),
                        'MOVE' : (self.move, float, float),
                        'TURN' : (self.turn, float, float)}
        self.receive()
    
    def receive(self):
        while True:
            recv = Control.receive().upper()
            if not recv.count(' '):
                Control.send('CONTROL FAIL Missing sender name')
                continue
            self.__active_task, data = recv.split(None, 1)
            if self.__hard_signal(data):
                continue
            else:
                self.__command_queue.put(recv)
            self.__active_task, data = \
                self.__command_queue.get().upper().split(None, 1)
            if match('^FAIL\ $', data):
                #TODO: Error handling
                pass
            elif not match('^(MOVE|TURN\ [0-9]+(\.[0-9]+)?|\.[0-9]+)|' + \
                           '(SET\ MOVE|TURN)\ [0-9]+(\.[0-9]+)?|\.[0-9]+$', data):
                Control.send(self.__active_task + ' FAIL Unknown message format')
            else:
                func, parm1, parm2 = data.split()
                load, cast1, cast2 = self.__FUNCS[func]
                load(cast1(parm1), cast2(parm2))
    
    def __hard_signal(self, data):
        if data == 'ALARM':
            self.__flush()
            Control.send(self.__active_task + ' FAIL Alarm signal received')
            return True
        elif data == 'STOP':
            Control.send(self.__active_task + ' FAIL Stop signal received')
            Control.send('MAIN OK')
            sys.exit()
            return True
        return False
    
    def add(self, set_type, step_size):
        if set_type.upper() == 'MOVE':
            self.step_dist = step_size
        elif set_type.upper() == 'TURN':
            self.step_angle = step_size
    
    def move(self, speed, distance):    
        pass
    
    
    def turn(self, speed, angle):
        pass
    
    
    def __flush(self):
        while not self.__command_queue.empty():
            self.__command_queue.get()
    
    
    def __odometry(self):
        if not Control.send('SENSORS GET ODOMETRY'):
            return
        
        while True:
            recv = Control.receive(True)
            if not recv or not recv.count(' '):
                Control.send('CONTROL FAIL Expecting message from sensors')
                return
            
            module, data = recv.upper().split(None, 1)
            if self.__hard_signal(data):
                return
            if module == 'SENSORS':
                return data.split(None)
            else:
                if self.__command_queue.full():
                    if not Control.send(self.__active_task + \
                                        ' FAIL Queue is full'):
                        return
                else:
                    self.__command_queue.put(recv)