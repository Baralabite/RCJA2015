from Amelior.model import leg


class Legs:
    def __init__(self, config):

        self.config = config
        self.legs = []

        self.initLegs()

    def moveBody(self, position):
        for leg in self.legs:
            leg.moveBody(position)

    """
    Initializes the legs
    """
    def initLegs(self):
        self.legs.append(leg.Leg(1, self.config))
        self.legs.append(leg.Leg(2, self.config))
        self.legs.append(leg.Leg(3, self.config))
        self.legs.append(leg.Leg(4, self.config))
        self.legs.append(leg.Leg(5, self.config))
        self.legs.append(leg.Leg(6, self.config))

    def updateOffsets(self):
        for leg in self.legs:
            leg.updateOffsets()

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
