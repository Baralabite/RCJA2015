from BaralabaBob.model import script

#TODO: Add in better event/callback support

class WalkForward(script.Script):    
    def __init__(self, hexapod):
        self.repeat = True
        self.hexapod = hexapod
        

    #Private Function
    def setSpeed(self, speed):
        self.SPEED = speed
        self.hexapod.legs.getLeg(1).setSpeed(self.SPEED)
        self.hexapod.legs.getLeg(3).setSpeed(self.SPEED)
        self.hexapod.legs.getLeg(5).setSpeed(self.SPEED)
        self.hexapod.legs.getLeg(6).setSpeed(self.SPEED)
        self.hexapod.legs.getLeg(4).setSpeed(self.SPEED)
        self.hexapod.legs.getLeg(2).setSpeed(self.SPEED)
        self.hexapod.tail.pitch.setSpeed(self.SPEED)
        self.hexapod.mandibles.pitch.setSpeed(self.SPEED)

    def onStart(self):
        self.setSpeed(10)
        self.hexapod.turnOn()        
        self.onAction()

    def onAction(self):
        def walkSequence(onFinish=None):
            one = lambda: self.lowerLegPair2(onFinish=two)
            two = lambda: self.liftLegPair1(onFinish=three)
            def three():
                self.moveLegPair1Forward()
                self.moveLegPair2Backward(onFinish=four)
            four = lambda: self.lowerLegPair1(onFinish=five)
            five = lambda: self.liftLegPair2(onFinish=six)
            def six():                
                self.moveLegPair1Backward()
                self.moveLegPair2Forward(onFinish=seven)
            seven = lambda: self.lowerLegPair2(onFinish=onFinish)
            one()
        walkSequence(onFinish=self.onRepeat)        

    def onRepeat(self):
        if self.repeat:
            self.onStart()
        else:
            self.onStop()

    def onStop(self, onFinish=None):
        self.repeat = False
        one = lambda: self.centerLegPair2(onFinish=two)
        two = lambda: self.lowerLegPair2(onFinish=three)
        three = lambda: self.liftLegPair1(onFinish=four)
        four = lambda: self.centerLegPair1(onFinish=five)
        five = lambda: self.lowerLegPair1(onFinish=onFinish)
        


    #Leg 1 stuff
    def liftLegPair1(self, onFinish=None):
        self.hexapod.legs.getLeg(1).femur.setAngle(50)
        self.hexapod.legs.getLeg(4).femur.setAngle(130)
        self.hexapod.legs.getLeg(5).femur.setAngle(50, callback=onFinish)

    def lowerLegPair1(self, onFinish=None):
        self.hexapod.legs.getLeg(1).femur.setAngle(90)
        self.hexapod.legs.getLeg(4).femur.setAngle(90)
        self.hexapod.legs.getLeg(5).femur.setAngle(90, callback=onFinish)

    def moveLegPair1Forward(self, onFinish=None):
        self.hexapod.legs.getLeg(1).hip.setAngle(70)
        self.hexapod.legs.getLeg(4).hip.setAngle(110)
        self.hexapod.legs.getLeg(5).hip.setAngle(70, callback=onFinish)

    def moveLegPair1Backward(self, onFinish=None):
        self.hexapod.legs.getLeg(1).hip.setAngle(110)
        self.hexapod.legs.getLeg(4).hip.setAngle(70)
        self.hexapod.legs.getLeg(5).hip.setAngle(110, callback=onFinish)

    def centerLegPair1(self, onFinish=None):
        self.hexapod.legs.getLeg(1).hip.setAngle(90)
        self.hexapod.legs.getLeg(4).hip.setAngle(90)
        self.hexapod.legs.getLeg(5).hip.setAngle(90, callback=onFinish)


    #Leg 2 stuff
    def liftLegPair2(self, onFinish=None):
        self.hexapod.legs.getLeg(2).femur.setAngle(130)
        self.hexapod.legs.getLeg(3).femur.setAngle(50)
        self.hexapod.legs.getLeg(6).femur.setAngle(130, callback=onFinish)

    def lowerLegPair2(self, onFinish=None):
        self.hexapod.legs.getLeg(2).femur.setAngle(90)
        self.hexapod.legs.getLeg(3).femur.setAngle(90)
        self.hexapod.legs.getLeg(6).femur.setAngle(90, callback=onFinish)

    def moveLegPair2Forward(self, onFinish=None):
        self.hexapod.legs.getLeg(2).hip.setAngle(110)
        self.hexapod.legs.getLeg(3).hip.setAngle(70)
        self.hexapod.legs.getLeg(6).hip.setAngle(110, callback=onFinish)

    def moveLegPair2Backward(self, onFinish=None):
        self.hexapod.legs.getLeg(2).hip.setAngle(70)
        self.hexapod.legs.getLeg(3).hip.setAngle(110)
        self.hexapod.legs.getLeg(6).hip.setAngle(70, callback=onFinish)

    def centerLegPair2(self, onFinish=None):
        self.hexapod.legs.getLeg(2).hip.setAngle(90)
        self.hexapod.legs.getLeg(3).hip.setAngle(90)
        self.hexapod.legs.getLeg(6).hip.setAngle(90, callback=onFinish)

    def centerAll(self, onFinish=None):
        one = lambda: self.liftLegPair1(onFinish=two)
        two = lambda: self.centerLegPair1(onFinish=three)
        three = lambda: self.lowerLegPair1(onFinish=four)
        four = lambda: self.liftLegPair2(onFinish=five)
        five = lambda: self.centerLegPair2(onFinish=six)
        six = lambda: self.lowerLegPair2(onFinish=onFinish)
        one()
