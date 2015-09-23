from Amelior.model import joint


class Tail:
    def __init__(self, configFile):

        self.config = eval(open(configFile, "r").read())

        self.pitch = joint.Joint("tailPitch", self.config, parentName="tailPitch")
        self.yaw = joint.Joint("tailYaw", self.config, parentName="tailYaw")

    def turnOn(self):
        self.pitch.turnOn()
        self.yaw.turnOn()

    def turnOff(self):
        self.pitch.turnOff()
        self.yaw.turnOff()
