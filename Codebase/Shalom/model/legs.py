from Amelior.model import leg


class Legs:
    def __init__(self, configFile, legConfigDir):

        self.legConfigDir = legConfigDir
        self.configFile = configFile
        self.config = eval(open(configFile, "r").read())
        self.legs = []

        self.initLegs()

    """
    Initializes the legs
    """
    def initLegs(self):
        self.legs.append(leg.Leg(1, self.legConfigDir))
        self.legs.append(leg.Leg(2, self.legConfigDir))
        self.legs.append(leg.Leg(3, self.legConfigDir))
        self.legs.append(leg.Leg(4, self.legConfigDir))
        self.legs.append(leg.Leg(5, self.legConfigDir))
        self.legs.append(leg.Leg(6, self.legConfigDir))

    """
    Returns the specified leg
    """
    def getLeg(self, id):
        return self.legs[id-1]

    def setSpeed(self, speed):
        for leg in self.legs:
            leg.setSpeed(speed)

    def turnOn(self):
        for leg in self.legs:
            leg.turnOn()

    def turnOff(self):
        for leg in self.legs:
            leg.turnOff()
