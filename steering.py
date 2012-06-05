class Steering:
    def __init__(self, step_dist, step_angle):
        self.__step_dist = step_dist
        self.__step_angle = step_angle
    
    def add(self, type, step_size):
        if (type == 'MOVE'):
            self.__step_dist = step_size
        else:
            self.__step_angle = step_size
    
    def move(self, speed, distance):
        pass
    
    def turn(self, speed, angle):
        pass