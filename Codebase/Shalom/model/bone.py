__author__ = 'John'

from Shalom.types.position3d import Position3D

class Bone:
    """
    head: Position3D of the head of the bone.
    angle: Int Angle of the direction of the bone.
    length: Length of the bone.
    """
    def __init__(self, head, angle, length):
        self.head = head
        self.setAngle(angle)
        self.length = length
        self.tail = Position3D(0, 0, 0)

        self.angleChangedCallback = None


    def setAngleChangedCallback(self, callback):
        self.angleChangedCallback = callback

    def setAngle(self, angle):
        self.angle = angle
        self.tail = self.head.getVectorTo(Position2D())
        self.angleChangedCallback(angle)


