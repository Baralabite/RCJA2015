"""
This class is intended to provide a quick and easy way to store 3D positions. It should also provide some functions to
help calculate distances, vectors, etc.
"""

from Amelior.util.position2d import Position2D
import math

class Position3D:
    def __init__(self, *args, tup=None):
        self.positionChangedCallback = None

        if len(args) == 1:
            self.x = args[0][0]
            self.y = args[0][1]
            self.z = args[0][2]
        elif len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]

        #Tup is now depircated.
        if not tup == None:
            self.setPositionTuple(tup)

        self.positionChangedCallback = None

    def __str__(self):
        return "Position3D({},{},{})".format(round(self.x, 2), round(self.y, 2), round(self.z, 2))

    def setPositionTuple(self, tup):
        self.x = tup[0]
        self.y = tup[1]
        self.z = tup[2]
        if not self.positionChangedCallback == None:
            self.positionChangedCallback(tup)

    def setPosition(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        if not self.positionChangedCallback == None:
            self.positionChangedCallback((x, y, z))

    def getDifference(self, position):
        return position.x-self.x, position.y-self.y, position.z-self.z

    """
    Returns Position3D for Azimuth, Elevation,Length (Spherical) coordinate
    """
    def sphericalToCartesian(self, angle, elevation, length):
        elevation = 90-elevation
        x = length * math.sin(math.radians(elevation)) * math.cos(math.radians(angle))
        y = length * math.sin(math.radians(elevation)) * math.sin(math.radians(angle))
        z = length * math.cos(math.radians(elevation))
        return Position3D(self.x+x, self.y+y, self.z+z)

    """
    Returns Position2D of two of the specified axes

    axes format: "XY", "YZ", "XZ", etc

    Returns None on error
    """
    def toPosition2D(self, axes):
        t = []
        if "X" in axes:
            t.append(self.x)
        if "Y" in axes:
            t.append(self.y)
        if "Z" in axes:
            t.append(self.z)

        if not len(t) == 2:
            return None

        return Position2D(0, 0, tup=t)

    """
    Returns Position3D of the two positions added together.
    """
    def addPosition(self, position):
        return Position3D(self.x+position.x, self.y+position.y, self.z+position.z)

    def setPositionChangedCallback(self, callback):
        self.positionChangedCallback = callback



