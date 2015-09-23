import math

class Position2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.positionChangedCallback = None

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

    """
    Returns Position2D for Angle,Length (Polar) coordinate
    """
    def polarToCartesian(self, angle, length):
        x = length * math.cos(math.radians(angle))
        y = length * math.sin(math.radians(angle))
        return (x, y)

    """
    Returns a vector (angle, direction) to specified position
    """
    def getVectorTo(self, position):
        return math.degrees(math.atan(abs(position.y-self.y)/abs(position.x-self.x)))