import logging
from os import path

from Amelior.model import joint
from Amelior.config.config import *


class Leg:
    def __init__(self, id, configDir):
        self.logger = logging.getLogger(Config.LOGGING_NAME+".Hexapod.Legs.Leg{}".format(id))
        self.id = id
        self.configFile = "leg{}.cfg".format(self.id)
        self.config = eval(open(path.join(configDir, self.configFile), "r").read())

        self.hip = joint.Joint("leg{}Hip".format(self.id), self.config)
        self.femur = joint.Joint("leg{}Femur".format(self.id), self.config)
        self.tibia = joint.Joint("leg{}Tibia".format(self.id), self.config)

        self.speed = 90

    """Dumps the settings for the leg to the display"""
    def printSettings(self):
        print("\nLeg %d Statistics:" % self.id)
        print("  Home Angle: %f" % self.config["homeAngle"])

    """Turns the leg on"""
    def turnOff(self):
        self.hip.turnOff()
        self.femur.turnOff()
        self.tibia.turnOff()

    """Turns the leg on"""
    def turnOn(self):
        self.hip.turnOn()
        self.femur.turnOn()
        self.tibia.turnOn()

    """Speed is expressed in degrees/second"""
    def setSpeed(self, speed):
        self.speed = speed
        self.hip.setSpeed(self.speed)
        self.femur.setSpeed(self.speed)
        self.tibia.setSpeed(self.speed)



