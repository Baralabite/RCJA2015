"""
This class is intended to provide a quick and easy way to store 3D positions. It should also provide some functions to
help calculate distances, vectors, etc.
"""

from Shalom.event.eventhandler import EventHandler
from Shalom.event.eventtypes import EventTypes

class Position3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.positionChangedCallback = None

    def setPosition(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        if not self.positionChangedCallback == None:
            self.positionChangedCallback((x, y, z))


    def setPositionChangedCallback(self, callback):
        self.positionChangedCallback = callback



