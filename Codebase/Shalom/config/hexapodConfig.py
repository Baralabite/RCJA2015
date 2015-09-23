__author__ = 'John'

class HexapodConfig:

    """
    ========== General Configuration ==========
    The robot's side to side axis is the X axis. The robot's forward and backwards axis is it's Y axis. The robot's up
    and down movement is considered the Z axis.

    The robot's legs are numbered left to right, front to back. Front left is 1, front right is 2, back right is 6, etc.

    The origin of all three axis (x, y, z) can be found below:
    X Axis: The centre of the servo horns of legs 3 and 4
    Y Axis: The centre of the top body plate. Also the line created by drawing a line through the two screws lying on the Y axis of the tail yaw servo horn.
    Z Axis: The top of the top-most body plate. All height measurements should be taken from this.

    """

    #Technically this should always stay the same, but just in case...
    self.hexapodOrigin = (0, 0, 0)

    """
    ========== Leg Config ==========

    All positions are taken from the defined origin of the robot as listed above.

    All measurements taken in MM

    leg#CoxaPosition: Defines position in 3D space where the coxa is relative to the centre of the robot.
    """

    leg1CoxaPosition = Position(-0, 0, 0)
    leg1FemurPosition = Position(-0, 0, -0)
    leg1TibiaPosition = Position(-0, 0, -0)

    leg1FemurLength = 60
    leg1TibiaLength = 60

    leg1CoxaAngle = 0
    leg1FemurAngle = 0
    leg1TibiaAngle = 0

    leg1CoxaInverted = False
    leg1FemurInverted = False
    leg1TibiaInverted = False



