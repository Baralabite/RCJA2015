import logging
import threading

from Amelior.event.eventhandler import *
from Amelior.event.eventtypes import *
from Amelior.config.config import *

class Joint:
    def __init__(self, name, config, parentName=None):
        self.name = name
        self.config = config
        self.logger = logging.getLogger(Config.LOGGING_NAME+".Hexapod.Legs."+name)

        if parentName == None:
            self.parentName = self.name[4:].lower()
        else:
            self.parentName = parentName

        self.pin = self.config[self.parentName+"Pin"]
        self._angle = 0
        self.speed = 130

        self.angleChangedCallback = None

        self.setOffset()

    def setAngleChangedCallback(self, callback):
        self.angleChangedCallback = callback

    def setSpeed(self, speed):
        self.speed = speed

    def setOffset(self):
        self.logger.debug("Setting offset of to "+str(self.config[self.parentName+"Offset"]))
        EventHandler.callEvent(EventTypes.JOINT_SERVO_OFFSET_CHANGE, (self.pin, self.config[self.parentName+"Offset"]))

    #============================================================#

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self.setAngle(angle)


    def getAngleSetTime(self, angle):
        return (abs(angle-self._angle) / self.speed)*1000

    def setAngle(self, angle, callback=None, angleCallback=None, callbackAngle=None, time=None):
        """
        Makes sure the angle is within the constraints

        TODO: This is to be replaced with dynamic constraint checking. I.e. BBox collision detection
        """

        offsetLimits = abs(self.config[self.parentName+"Offset"]/8.0)

        try:
            if angle < self.config[self.name+"Min"]+offsetLimits:
                angle = self.config[self.name+"Min"]+offsetLimits
            elif angle > self.config[self.name+"Max"]-offsetLimits:
                angle = self.config[self.name+"Max"]-offsetLimits
        except KeyError:
            #self.logger.warn("Angle min/max not configured for {}".format(self.name))
            if angle < -90+offsetLimits:
                angle = -90+offsetLimits
            elif angle > 90-offsetLimits:
                angle = 90-offsetLimits

        if not time:
            time = (abs(angle-self._angle) / self.speed)*1000   #Calculates time required to execute move at current speed
        self.setSignal(self.angleToSignal(angle), time)     #Sets the servo signal

        """
        Fires the specified callback when the leg reaches a specific angle
        """
        if angleCallback:
            if callbackAngle:
                threading.Timer(abs(callbackAngle-self._angle)/self.speed, angleCallback).start()
            else:
                self.logger.error("No angle specified.")
        """
        Fires the callback when the movement has finished.
        """
        if callback:
            threading.Timer(time/1000, callback).start()

        EventHandler.callEvent(EventTypes.JOINT_ANGLE_CHANGE, (self.name, angle))
        self._angle = angle

        """
        Calls the specified angleChanged callback when the angle changes
        """
        if self.angleChangedCallback:
            self.angleChangedCallback()

    def getAngle(self):
        return self._angle

    #============================================================#

    def angleToSignal(self, angle):
        if self.name.startswith("leg"):
            if angle == 0.0:
                angle = abs(angle)  #To catch any cases of -0.0 which throws everything around
            return int(((((1000/90)*angle)*int(self.config[self.parentName+"Inversion"]))+1500))
        else:
            return int((((1000/90)*angle)+1500))

    def setSignal(self, signal, time):
        EventHandler.callEvent(EventTypes.JOINT_SERVO_SIGNAL_CHANGE, (self.name, self.pin, signal, time))
        self.signal = 1500

    def turnOff(self):
        self.angle = 0
        self.setSignal(0, 0)

    def turnOn(self):
        self.setAngle(0)