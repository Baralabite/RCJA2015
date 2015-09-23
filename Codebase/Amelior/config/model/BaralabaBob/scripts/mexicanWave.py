from BaralabaBob.model import script
import time


class MexicanWave(script.Script):
    def __init__(self, hexapod):
        self.hexapod = hexapod

        self.repeat = False
        self.SPEED = 50 #Speed expressed in degrees/sec
        self.setSpeed(50)        

        self.finishCallback = None


    def setFinishCallback(self, callback):
        self.finishCallback = callback
        
    #Private Function
    def setSpeed(self, speed):
        self.SPEED = speed
        self.hexapod.legs.getLeg(1).femur.setSpeed(self.SPEED)
        self.hexapod.legs.getLeg(3).femur.setSpeed(self.SPEED)
        self.hexapod.legs.getLeg(5).femur.setSpeed(self.SPEED)
        self.hexapod.legs.getLeg(6).femur.setSpeed(self.SPEED)
        self.hexapod.legs.getLeg(4).femur.setSpeed(self.SPEED)
        self.hexapod.legs.getLeg(2).femur.setSpeed(self.SPEED)
        self.hexapod.tail.pitch.setSpeed(self.SPEED)
        self.hexapod.mandibles.pitch.setSpeed(self.SPEED)
        
    #Future override functions
    def onStart(self):
        self.startTime = time.time()

        #Up Left
        leg1Up = lambda: self.hexapod.legs.getLeg(1).femur.setAngle(0, callback=leg1Down, angleCallback=leg3Up, callbackAngle=30)
        leg3Up = lambda: self.hexapod.legs.getLeg(3).femur.setAngle(0, callback=leg3Down, angleCallback=leg5Up, callbackAngle=30)
        leg5Up = lambda: self.hexapod.legs.getLeg(5).femur.setAngle(0, callback=leg5Down, angleCallback=leg6Up, callbackAngle=30) #Took tail out

        #Tail Up
        #tailUp = lambda: self.hexapod.tail.pitch.setAngle(130, callback=tailDown, angleCallback=leg6Up, callbackAngle=130)
        
        #Up Right
        leg6Up = lambda: self.hexapod.legs.getLeg(6).femur.setAngle(180, callback=leg6Down, angleCallback=leg4Up, callbackAngle=150)
        leg4Up = lambda: self.hexapod.legs.getLeg(4).femur.setAngle(180, callback=leg4Down, angleCallback=leg2Up, callbackAngle=150)
        leg2Up = lambda: self.hexapod.legs.getLeg(2).femur.setAngle(180, callback=leg2Down)#, angleCallback=mandiblesUp, callbackAngle=150)

        #Mandibles Up
        #mandiblesUp = lambda: self.hexapod.mandibles.pitch.setAngle(50, callback=mandiblesDown, angleCallback=self.onRepeat, callbackAngle=130)
        

        #Down Left
        leg1Down = lambda: self.hexapod.legs.getLeg(1).femur.setAngle(90)
        leg3Down = lambda: self.hexapod.legs.getLeg(3).femur.setAngle(90)
        leg5Down = lambda: self.hexapod.legs.getLeg(5).femur.setAngle(90)

        #Tail Down
        #tailDown = lambda: self.hexapod.tail.pitch.setAngle(90)
        
        #Down Right
        leg6Down = lambda: self.hexapod.legs.getLeg(6).femur.setAngle(90)
        leg4Down = lambda: self.hexapod.legs.getLeg(4).femur.setAngle(90)
        leg2Down = lambda: self.hexapod.legs.getLeg(2).femur.setAngle(90, callback=self.onRepeat)

        #Mandibles Down
        #mandiblesDown = lambda: self.hexapod.mandibles.pitch.setAngle(90, callback=self.onRepeat)

        leg1Up()


    def onRepeat(self):
        if self.repeat:
            self.onStart()
        else:
            self.onStop()

    def onStop(self):
        self.repeat = False
        self.stopTime = time.time()
        self.totalTime = (self.stopTime-self.startTime)*1000
        print("Milliseconds: {}".format(self.totalTime))
        
        if self.finishCallback:
            self.finishCallback()
    
        
