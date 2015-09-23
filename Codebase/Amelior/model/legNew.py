from Amelior.model.bone import Bone

class Leg:
    def __init__(self, id, globalConfig):
        self.logger = logging.getLogger(Config.LOGGING_NAME+".Hexapod.Legs.Leg{}".format(id))
        self.logger.debug("Leg {} initializing.".format(id))

        """
        ID is in the format of 1-6. Left right, front back.
        """
        self.id = id

        """
        Global config is the hexapod.cfg file. Leg specific cfg is extracted from it
        """
        self.globalConfig = globalConfig

        """
        Leg specific config.
        """
        self.config = self.globalConfig["leg{}Config".format(id)]

        """
        This section contains the bones.
        BoneID: leg1Coxa, leg2Femur, leg5Tibia, etc
        """
        self.coxaBone = Bone("leg{}Coxa".format(id))
        self.femurBone = Bone("leg{}Femur".format(id))
        self.tibiaBone = Bone("leg{}Tibia".format(id))


