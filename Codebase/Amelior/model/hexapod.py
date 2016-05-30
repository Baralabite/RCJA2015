from os import path
from time import sleep
import time
import traceback

from Amelior.event.eventhandler import *
from Amelior.event.eventtypes import *
from Amelior.comms import robotcommunication
from Amelior.config.config import *
from Amelior.model import mandibles, legs, tail
from Amelior.config.configparser import ConfigParser
from Amelior.util.position3d import Position3D
import Amelior



class Hexapod:
    def __init__(self):
        self.logger = logging.getLogger(Config.LOGGING_NAME+".Hexapod")
        self.logger.info("Initializing Hexapod...")

        self.configParser = ConfigParser("BaralabaBob")
        self.configDir = path.join(path.dirname(Amelior.__file__), "config/model/BaralabaBob")
        self.config = self.configParser.loadConfig("hexapod.cfg")

        self.logger.debug("Connecting to TCP Serial Bridge...")
        self.comms = robotcommunication.RobotCommunication()
        self.comms.connect((Config.TCP_SERIAL_BRIDGE_IP, Config.TCP_SERIAL_BRIDGE_PORT))
        self.logger.debug("Changing to Servo Comms mode...")
        self.comms.send(bytes("S\r", "utf-8"))
        sleep(0.3)
        self.logger.info("Connected to TCP Serial Bridge")
        self._position = Position3D(0, 0, 0)

        EventHandler.addListener("serialUpdater", EventTypes.JOINT_SERVO_SIGNAL_CHANGE, self.updateServoSignal)
        EventHandler.addListener("updateOffset", EventTypes.JOINT_SERVO_OFFSET_CHANGE, self.updateServoPositionOffset)

        #Reads in the home directory of the config files, and joins it to the leg config location
        self.legs = legs.Legs(self.config)

        mandiblesConfig = path.join(self.configDir, self.config["mandiblesConfig"])
        self.mandibles = mandibles.Mandibles(mandiblesConfig)

        tailConfig = path.join(self.configDir, self.config["tailConfig"])
        self.tail = tail.Tail(tailConfig)

        self.on = False

        self.logger.info("Initialized Hexapod!")

    def translate(self, x, y, z):
        self._position = Position3D(self._position.x+x, self._position.y+y, self._position.z+z)
        self.legs.moveBody(Position3D(x, y, z))

    def setPosition(self, position):
        self._position = position
        self.legs.moveBody(position)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self.setPosition(position)


    def start(self):
        pass

    def turnOn(self):
        self.legs.setSpeed(self.config["defaultSpeed"])
        #setOffsetPositions()
        self.legs.turnOn()
        self.mandibles.turnOn()
        self.tail.turnOn()

        self.on = True

    def step(self):
        self.legs.setSpeed(120)
        self.legs.getLeg(1).translate(0, 20, 40)
        self.legs.getLeg(4).translate(0, 20, 40)
        self.legs.getLeg(5).translate(0, 20, 40)

        time.sleep(0.3)

        self.legs.getLeg(1).translate(0, 20, -40)
        self.legs.getLeg(4).translate(0, 20, -40)
        self.legs.getLeg(5).translate(0, 20, -40)

        time.sleep(0.3)

        self.legs.getLeg(2).translate(0, 20, 40)
        self.legs.getLeg(3).translate(0, 20, 40)
        self.legs.getLeg(6).translate(0, 20, 40)

        time.sleep(0.3)

        self.legs.getLeg(2).translate(0, 20, -40)
        self.legs.getLeg(3).translate(0, 20, -40)
        self.legs.getLeg(6).translate(0, 20, -40)

        time.sleep(0.3)

        self.translate(0, 40, 0)

        time.sleep(1)

    def updateOffsets(self):
        self.mandibles.updateOffsets()
        self.legs.updateOffsets()
        self.tail.updateOffsets()


    def turnOff(self):
        #self.turnOn()
        self.legs.turnOff()
        self.mandibles.turnOff()
        self.tail.turnOff()

        self.on = False

    def smoothTest(self):
        factor = 1.5
        time.sleep(0.5)
        self.turnOn()
        while True:
            self.legs.getLeg(6).tibia.setAngle(84, time=1000)
            time.sleep(1.0)
            self.legs.getLeg(6).tibia.setAngle(0, time=1000)
            time.sleep(1.0)

    def updateServoSignal(self, data):
        packet = "#%d P%d T%d\r" % (data[1], data[2], data[3])
        self.comms.send(bytes(packet, 'utf-8'));

    def updateServoPositionOffset(self, data):
        packet = "#%d PO %d\r" % (data[0], data[1])
        self.comms.send(bytes(packet, 'utf-8'))