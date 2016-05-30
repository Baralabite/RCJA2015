from Amelior.model import joint

class Mandibles:
    def __init__(self, configFile):
        self.config = eval(open(configFile, "r").read())

        self.leftJaw = joint.Joint("mandiblesLeftJaw", self.config, parentName="mandiblesLeftJaw")
        self.rightJaw = joint.Joint("mandiblesRightJaw", self.config, parentName="mandiblesRightJaw")
        self.pitch = joint.Joint("mandiblesPitch", self.config, parentName="mandiblesPitch")
        self.yaw = joint.Joint("mandiblesYaw", self.config, parentName="mandiblesYaw")
        self.roll = joint.Joint("mandiblesRoll", self.config, parentName="mandiblesRoll")

    def updateOffsets(self):
        self.leftJaw.setOffset()
        self.rightJaw.setOffset()
        self.pitch.setOffset()
        self.yaw.setOffset()
        self.roll.setOffset()

    def turnOn(self):
        self.leftJaw.turnOn()
        self.rightJaw.turnOn()
        self.pitch.turnOn()
        self.yaw.turnOn()
        self.roll.turnOn()

    def turnOff(self):
        self.leftJaw.turnOff()
        self.rightJaw.turnOff()
        self.pitch.turnOff()
        self.yaw.turnOff()
        self.roll.turnOff()

    def closeJaw(self):
        self.leftJaw.setAngle(90)
        self.rightJaw.setAngle(90)

    def openJaw(self):
        self.leftJaw.setAngle(140)
        self.rightJaw.setAngle(40)

