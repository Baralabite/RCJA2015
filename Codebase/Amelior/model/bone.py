from Amelior.util.position2d import Position2D
from Amelior.util.position3d import Position3D

class Bone:
    def __init__(self, id, globalConfig, headPosition, tailPosition):
        self.id = id

        """
        Global config is the hexapod.cfg
        """
        self.globalConfig = globalConfig

        """
        Extracts the leg specific config from the global config
        """
        self.config = self.globalConfig[self.getLegName()+"Config"]

        """
        Raw variables for head and tail position. Noted with preceeding underscore to allow for properties to be made
        """
        self._headPosition = headPosition
        self._tailPosition = tailPosition

        """
        Leg length from config using legConfig->coxaLength (for example)
        """
        self.legLength = self.config["legConfig"][self.boneType()+"Length"]

        """
        Axis on which to rotate the bone
        """
        self.rotationAxis = self.config["legConfig"][self.boneType()+"RotationAxis"]

        """
        Rotation on specified axis
        """
        self.rotation = 0

    @property
    def headPosition(self):
        return self._headPosition

    @property.setter
    def headPosition(self, value):
        self._headPosition = value

    @property
    def tailPosition(self):
        return self._tailPosition

    @property.setter
    def tailPosition(self, value):
        self._tailPosition = value

    """
    Returns name of leg in format: leg# (leg1, leg4, etc)
    Useful for transforming leg4Coxa into leg4Config for example.
    """
    def getLegName(self):
        return self.id[:4]

    """
    Returns type of bone. i.e. femur, coxa, tibia
    """
    def getBoneType(self):
        return self.id[4:].lower()
