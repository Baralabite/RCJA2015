import logging, math
from os import path

from Amelior.model import joint
from Amelior.config.config import *

from Amelior.util.position2d import Position2D
from Amelior.util.position3d import Position3D

from Amelior.model.joint import Joint

class Leg:
    def __init__(self, id, config):
        self.logger = logging.getLogger(Config.LOGGING_NAME+".Hexapod.Legs.Leg{}".format(id))
        self.id = id
        self.globalConfig = config
        self.config = self.globalConfig["leg{}Config".format(id)]

        #FK/IK information
        self._position = Position3D(self.config["position"])
        self.globalAngle = self.config["homeAngle"]

        self.coxa = Joint("leg{}Coxa".format(self.id), self.config)
        self.coxa.setAngleChangedCallback(self.forwardKinematics)
        self.coxaHead = self.position
        self.coxaTail = None

        self.femur = Joint("leg{}Femur".format(self.id), self.config)
        self.femur.setAngleChangedCallback(self.forwardKinematics)
        self.femurHead = None
        self.femurTail = None

        self.tibia = Joint("leg{}Tibia".format(self.id), self.config)
        self.tibia.setAngleChangedCallback(self.forwardKinematics)
        self.tibiaHead = None
        self.tibiaTail = None

        self.footPosition = None
        ###

        self.forwardKinematics()
        self.homePosition = self.tibiaTail
        self.relativeTibiaHome = self.coxaHead.getDifference(self.tibiaTail)

        if "legSpeed" in self.globalConfig:
            self.speed = self.globalConfig["legSpeed"]
        elif "legSpeed" in self.config:
            self.speed = self.config["legSpeed"]
        else:
            self.speed = 90
            self.setSpeed(self.speed)


    def updateOffsets(self):
        self.coxa.setOffset()
        self.femur.setOffset()
        self.tibia.setOffset()

    def moveBody(self, position):
        footPosition = self.footPosition
        self.setPosition(self.position.addPosition(position))
        self.setFootPosition(footPosition)

    #Sets the coxa head position. Uses decorators to detect changes in the position property.
    def setPosition(self, position):
        self._position = position
        self.forwardKinematics()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self.setPosition(position)

    """
    Calculates the position of each end of each bone based upon the current joint angles
    This function is called after any change to the leg position, joint angle  changes, etc
    """
    def forwardKinematics(self):
        self.coxaHead = self._position

        self.femurHead = self.position.sphericalToCartesian((self.coxa.getAngle()*self.config["coxaInversion"])+self.globalAngle, 0, self.globalConfig["legConfig"]["coxaLength"])
        self.femurHead = self.femurHead.addPosition(Position3D(0, 0, self.config["femurZOffset"]))
        self.coxaTail = self.femurHead

        self.tibiaHead = self.femurHead.sphericalToCartesian((self.coxa.getAngle()*self.config["coxaInversion"])+self.globalAngle, self.femur.getAngle(), self.globalConfig["legConfig"]["femurLength"])
        self.femurTail = self.tibiaHead

        self.tibiaTail = self.tibiaHead.sphericalToCartesian((self.coxa.getAngle()*self.config["coxaInversion"])+self.globalAngle, (self.femur.angle+self.tibia.angle)-90, self.globalConfig["legConfig"]["tibiaLength"])
        self.footPosition = self.tibiaTail


    """
    Moves the robot's leg relative to it's current position
    """
    def translate(self, x, y, z):
        pos = Position3D(self.footPosition.x+x, self.footPosition.y+y, self.footPosition.z+z)
        self.setFootPosition(pos)

    """
    Turns the leg on
    """
    def turnOn(self):
        self.coxa.turnOn()
        self.femur.turnOn()
        self.tibia.turnOn()

    """
    Turns the leg off
    """
    def turnOff(self):
        self.coxa.turnOff()
        self.femur.turnOff()
        self.tibia.turnOff()

    """
    Speed is expressed in degrees/second
    """
    def setSpeed(self, speed):
        self.speed = speed
        self.coxa.setSpeed(self.speed)
        self.femur.setSpeed(self.speed)
        self.tibia.setSpeed(self.speed)

    def move(self, x, y, z):
        self.setFootPosition(Position3D(x, y, z))

    """
    Does fancy IK stuff to calculate foot angles and stuff.

    Position is a Position3D class
    """
    def setFootPosition(self, position):
        try:
            x = position.x
            y = position.y
            z = position.z
            position = Position3D(x, y, z)
            coxa = Position2D(self.coxaHead.x, self.coxaHead.y)
            target = Position2D(position.x, position.y)
            L1 = coxa.getDistance(target)
            diff = coxa.getDifference(target)

            try:
                g = math.degrees(math.atan(diff[0]/diff[1]))
            except ZeroDivisionError:
                print("Div/0")
                g = 90#math.degrees(math.atan(0.0))

            g = (180-abs(g))-90

            if (self.position.y-diff[1]) < (self.position.y+self.relativeTibiaHome[1]):# and self.id not in [3, 4]:
                g = g * -1



            head = Position2D(self.femurHead.x, self.femurHead.z)
            target = Position2D(position.x, position.z)
            L = math.sqrt(head.getDifference(target)[1]**2+(L1-self.globalConfig["legConfig"]["coxaLength"])**2)
            a1 = math.degrees(math.acos((head.getTuple()[1]-target.getTuple()[1])/L))
            a2 = math.degrees(math.acos(((self.globalConfig["legConfig"]["tibiaLength"]**2)-(self.globalConfig["legConfig"]["femurLength"]**2)-(L**2))/(-2 * self.globalConfig["legConfig"]["femurLength"] * L)))
            a = a1 + a2
            b = math.degrees(math.acos(((L**2) - (self.globalConfig["legConfig"]["tibiaLength"]**2) - (self.globalConfig["legConfig"]["femurLength"]**2))/(-2*self.globalConfig["legConfig"]["tibiaLength"]*self.globalConfig["legConfig"]["femurLength"])))
            a = a - 90
            b = (b-180)+90
            g = self.config["coxaAngleOffset"]-g

            speeds = []
            speeds.append(self.femur.getAngleSetTime(a))
            speeds.append(self.tibia.getAngleSetTime(b))
            speeds.append(self.coxa.getAngleSetTime(g))

            time = max(speeds)

            self.femur.setAngle(a, time=time)
            self.tibia.setAngle(b, time=time)
            self.coxa.setAngle(g, time=time)

            return time

        except ZeroDivisionError:
            print("Div by 0 stuff. Do nothing")