import control


class Steering:
    def __init__(self, step_dist, step_angle):
        self.step_dist = step_dist
        self.step_angle = step_angle
        self.__
    
    def add(self, set_type, step_size):
        if set_type == 'MOVE':
            self.__step_dist = step_size
        elif set_type == 'TURN':
            self.__step_angle = step_size
    
    def move(self, speed, distance):
        
        pass
    
    def turn(self, speed, angle):
        pass
    
    def __odometry(self):
        if not control.send('SENSORS GET ODOMETRY'):
            return None
        module, data = control.receive(True).split(' ', 1)
            