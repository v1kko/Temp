'''
@since: 04 Jun 2012
@author: Cedric Blom
@version: 1.0

@summary: This program translates relative robot "MOVE" and "TURN" instructions 
in wheel rotation instructions. Instructions are executed in a FIFO order.
Instructions will either be completely executed or it fails. A failure will
always trigger a emergency stop followed by a FAIL message with detailed
information about the failure reason.
'''

from Queue import Queue
from re import match
import math
import Control

class Steering:
    #Start up the module
    def __init__(self, grid_size = 1.0):
        self.ctrl = Control.Control(self.__class__.__name__)
        self.stop_signal = False
        self.grid_size = grid_size
        self.__command_queue = Queue()
        self.__active_task = ''
        self.__FUNCS = {'SET' : (self.add, str, float),
                        'MOVE' : (self.move, float, float),
                        'TURN' : (self.turn, float, float)}
        self.receive()
        exit(0)

    # @note: Receive and handle messages (and make sure you can handle
    #  'incorrect' messages)
    def receive(self):
        #For a stop signal we'd drop our regular work
        while not self.stop_signal:
            recv = self.ctrl.receive()
            #Ignore empty messages, start listening again
            if recv == None:
                continue
            self.__active_task, data = recv
            data = data.upper()
            #If it is a signal and it returns True we don't put anything else 
            #into the queue and flush it ##########are we warning the robot to stop
            if self.__hard_signal(data):
                continue
            #Otherwise, add the received command to the queue
            else:
                self.__command_queue.put(recv)

            #Time to check whether the command adhers to protocol##
            self.__active_task, data = self.__command_queue.get()
            data = data.upper()
            if match('^FAIL\ .*$', data):
                #TODO: Error handling
                pass
            #Check whether you receive a float/int when you expect to
            elif not match('^(MOVE|TURN\ [0-9]+(\.[0-9]+)?|\.[0-9]+)|' + \
                           '(SET\ MOVE|TURN)\ [0-9]+(\.[0-9]+)?|\.[0-9]+$', data):
                self.ctrl.send(self.__active_task, 
                               'FAIL Unknown message format: %s' % (data))
            else:
                func, parm1, parm2 = data.split()
                load, cast1, cast2 = self.__FUNCS[func]
                load(cast1(parm1), cast2(parm2))

    # @note: Handle signals of various types.
    #  ALARM: robot is about to crash into something, stop
    #  STOP: The module is told to stop
    #  ISEMPTY: Tell the testmodule the data was empty
    # @param: str $data Can be types ALARM, STOP or ISEMPTY
    # @return: bool If True the robot will be told to stop in its tracks
    def __hard_signal(self, data):
        #Returning True will stop the robot in its tracks
        if data == 'ALARM':
            self.__flush()
            self.ctrl.send(self.__active_task, 'FAIL Alarm signal received')
            return True
        elif data == 'STOP':
            self.stop_signal = True
            return True
        elif data == 'ISEMPTY':
            self.ctrl.send('Test', 'ISEMPTY %r' % (self.__command_queue.empty()))
        return False

    # @note: Set the size of a single step forward in MOVE
    # @param str $set_type The type to change (can only be MOVE now)
    def add(self, set_type, step_size):
        if set_type.upper() == 'MOVE':
            self.grid_size = step_size

    # @note: Move the robot for a certain distance either forward or backward
    #  If odometry is None: stop the robot and inform the calling task
    #  Note that if parameters aren't floats/ints your command won't be executed
    #  If the command was executed succesfully it will inform the calling task
    # @param: float $speed The speed at which to move the robot
    # @param: float $distance The distance the robot should move
    def move(self, speed, distance):
        grid_dist = distance * distance * self.grid_size
        start = True
        while True:
            odo = self.__odometry()

            #If odometry is None tell the robot to stop moving and inform the 
            #task calling that the move failed
            if not odo:
                ins = 'DRIVE {Left %f} {Right %f}\r\n' % (0.0, 0.0)
                self.ctrl.send('Interface', ins)
                self.ctrl.send(self.__active_task, 'FAIL Robot movement aborted')
                return

            #For the first iteration of the loop only:
            if start:
                #Save your current position, the startpoint of the move
                xs, ys = odo[0:2]
                #Tell the robot through Interface to continuously move forward
                ins = 'DRIVE {Left %f} {Right %f}\r\n' % (speed, speed)
                self.ctrl.send('Interface', ins)
                start = False

            #Get the current position and find out difference with starting pos
            xa, ya = odo[0:2]
            xr = xa - xs
            yr = ya - ys

            #If we have travelled the requested relative distance:
            if xr*xr + yr*yr >= grid_dist:
                #Tell the robot to stop
                ins = 'DRIVE {Left %f} {Right %f}\r\n' % (0.0, 0.0)
                self.ctrl.send('Interface', ins)
                #Tell the active task his request has been completed
                self.ctrl.send(self.__active_task, 'OK')
                #End the function
                return

    # @note: Turn the robot a certain amount of degrees at a certain speed
    #  If odometry is None: stop the robot and inform the calling task
    #  Note that if parameters aren't floats/ints your command won't be executed
    #  If the command was executed succesfully it will inform the calling task
    # @param: float $speed The speed at which to turn the robot
    # @param: float $angle The angle in degrees the robot should turn:
    #  A positive angle means turning right, a negative one turning left
    def turn(self, speed, angle):
        start = True
        #Calculate the size of a radian in degrees
        angle = angle % 360.0
        rad = angle / 180.0 * math.pi

        while True:
            odo = self.__odometry()

            #If the odometer returns None:
            if not odo:
                #Tell the robot to stop
                ins = 'DRIVE {Left %f} {Right %f}\r\n' % (0.0, 0.0)
                self.ctrl.send('Interface', ins)
                #Inform the calling task that the command failed
                self.ctrl.send(self.__active_task, 'FAIL Robot movement aborted')
                return

            #On the first iteration:
            if start:
                #Remember the orientation in the starting position
                ts = odo[3]
                #Positive angle means turning right
                if angle < 0.0:
                    drive = (-speed, speed)
                else:
                    drive = (speed, -speed)
                #Tell the robot to start turning
                ins = 'DRIVE {Left %f} {Right %f}\r\n' % drive
                self.ctrl.send('Interface', ins)
                start = False

            #Get the current orientation and look at the difference with the
            #starting orientation
            ta = odo[3]
            tr = ta - ts
            #If we have turned the requested /relative/ angle:
            #(ie. when the robot starts at 0pi rad and turns 0.1 in either
            #direction xa-xs should be 0.1pi rad, and not 1.9pi rad in one
            #direction)
            if abs(tr) >= rad:
                #Tell the robot to stop turning
                ins = 'DRIVE {Left %f} {Right %f}\r\n' % (0.0, 0.0)
                self.ctrl.send('Interface', ins)
                #Tell the calling task his request has been completed
                self.ctrl.send(self.__active_task, 'OK')
                return

    # @note: Empty the queue
    def __flush(self):
        while not self.__command_queue.empty():
            self.__command_queue.get()

    # @note: Get the odometry value
    #  If the queue is full, a value expected to be a float is not a number or
    #  no message is received we send an error message and continue with the 
    #  rest of the program
    def __odometry(self):
        #Try to send a request for getting the odometry sensor's values
        if not self.ctrl.send('Sensors', 'GET ODOMETRY'):
            return

        while True:
            #Look for the message we wanted
            recv = self.ctrl.receive(True)
            #If nothing is received, tell the main we were expecting a message
            if not recv:
                self.ctrl.send('Main', 'FAIL Expecting message from sensors')
                return

            #Modulename uppercase so that faulty input in str format is corrected
            module, data = map(str.upper, recv)
            if self.__hard_signal(data):
                return

            if data == 'ISEMPTY':
                continue
            #Check whether you received a float/int
            if module == 'SENSORS' and match('^ODOMETRY\ ' + \
                '([0-9]+(\.[0-9]+)?|\.[0-9]+\ ){2}' + \
                '[0-9]+(\.[0-9]+)?|\.[0-9]+$', data):
                return map(float, data.split(None)[1:4])
            else:
                #If the queue is full, inform the task calling you of it and
                #continue with the rest of the program
                if self.__command_queue.full():
                    if not self.ctrl.send(self.__active_task, 'FAIL Queue is full'):
                        return
                #Otherwise, queue the command
                else:
                    self.__command_queue.put(recv)
