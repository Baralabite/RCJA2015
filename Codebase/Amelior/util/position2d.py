import math

class Position2D:
    def __init__(self, x, y, tup=None):
        self.x = x
        self.y = y

        if not tup == None:
            self.x = tup[0]
            self.y = tup[1]

        self.positionChangedCallback = None

    def __str__(self):
        return "Position2D({}, {})".format(self.x, self.y)

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.positionChangedCallback((x, y))

    """
    Sets the callback to be called when the position changes.
    """
    def setPositionChangedCallback(self, callback):
        self.positionChangedCallback = callback

    """
    Finds distance between itself and position
    """
    def getDistance(self, position):
        return math.sqrt(abs(position.x-self.x)**2 + abs(position.y-self.y)**2)

    def getTuple(self):
        return self.x, self.y

    def getDifference(self, position):
        return position.x-self.x, position.y-self.y

    """
    Returns Position2D for Angle,Length (Polar) coordinate
    """
    def polarToCartesian(self, angle, length):
        x = length * math.cos(math.radians(angle))
        y = length * math.sin(math.radians(angle))
        return Position2D(self.x+x, self.y+y)


    """
    Returns Position2D of the two positions added together
    """
    def addPosition(self, position):
        return Position2D(self.x+position.x, self.y+position.y)

    """
    Returns a vector (angle, direction) to specified position
    """
    def getVectorTo(self, position):
        return math.degrees(math.atan(abs(position.y-self.y)/abs(position.x-self.x)))