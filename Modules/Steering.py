from Queue import Queue
import Control


class Steering:
    def __init__(self, grid_size, angle_size):
        self.grid_size = grid_size
        self.angle_size = angle_size
        self.__command_queue = Queue()
        self.__active_task = ''
    
    
    def add(self, set_type, step_size):
        if set_type.upper() == 'MOVE':
            self.step_dist = step_size
        elif set_type.upper() == 'TURN':
            self.step_angle = step_size
    
    
    def move(self, speed, distance):    
        pass
    
    
    def turn(self, speed, angle):
        pass
    
    
    def flush(self):
        while not self.__command_queue.empty():
            self.__command_queue.get()
    
    
    def __odometry(self):
        if not control.send('SENSORS GET ODOMETRY'):
            return
        
        while True:
            recv = control.receive(True)
            if not recv or recv.find(' ') == -1:
                control.send('CONTROL FAIL Expecting message from sensors')
                return
            
            module, data = recv.upper().split(None, 1)
            if data == 'ALARM':
                self.flush()
                return
            if module == 'SENSORS':
                return data.split(None)
            else:
                if self.__command_queue.full() and \
                not control.send(self.__active_task + ' FAIL Queue is full'):
                    return
                else:
                    self.__command_queue.put(data)
