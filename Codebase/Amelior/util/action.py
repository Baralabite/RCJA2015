import base64, threading, time, os, Amelior
import RPi.GPIO as GPIO


class Action:
    def __init__(self, script, hexapod):
        self.script = {}
        self.hexapod = hexapod

        self.scriptDirectory = os.path.join(os.path.dirname(Amelior.__file__), "config/model/BaralabaBob/actions")

        self.overlap = 200

        #Default framerate is 24.0
        #Make lower to slow motion down, make higher to speed up action
        self.frameRate = 24.0

        self.openFile(script)
        self.frames = self.getFrames()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)



    def openFile(self, script):
        f = open(os.path.join(self.scriptDirectory, script+".act"), "r")
        data = f.read()
        try:
            strOutput = base64.b64decode(bytes(data,"utf-8")).decode("utf-8")
        except:
            strOutput = data
        self.script = eval(strOutput)
        try:
            self.animationLength = self.script["animationLength"]
            del self.script["animationLength"]
        except:
            pass
        try:
            self.bezierOverlap = self.script["bezierOverlap"]
            del self.script["bezierOverlap"]
        except:
            pass

    def getFrames(self):
        frames = [entry for entry in self.script]
        frames.sort()
        #frames = [f-frames[0] for f in frames]
        return frames


    def execute(self):
        #self.setStartingPositions()
        time.sleep(0.2)
        f = self.getFrames()
        del f[0]
        for x in f:
            t = self.playFrame(x)
            time.sleep(0.001*t)

    """
    Repeats a loop of the action.
    Int reps    Number of times to repeat the action
    %   speed   Speed as expressed in percent to execute action
    """
    def repeatAction(self, reps, speed=100):
        if speed != 100:
            self.frameRate=(speed/100)*24.0

        self.setStartingPositions()
        for rep in range(reps):
            f = self.getFrames()
            played = []
            totalTime = (max(f)/24)*1000
            startTime = time.time()*1000
            currFrame = None
            #self.playFrame(0, timeOfFrame=1)
            print("Start Time", startTime, totalTime)
            while (time.time()*1000)-startTime < totalTime:
                currTime = (time.time()*1000)-startTime
                if currFrame == None:
                    currFrame = 0
                else:
                    currFrame = int((currTime/1000)*24)

                if currFrame in f:
                    if not currFrame in played:
                        try:
                            nextFrame = f[f.index(currFrame)+1]
                        except:
                            print("No new frames!")
                            break
                        self.playFrame(nextFrame, timeOfFrame=((nextFrame-currFrame)/24)*1000)
                        if GPIO.input(24) == 0:
                            self.hexapod.turnOn()
                            break
                        played.append(currFrame)

            """for x in range(max(f)):
                a = time.time()
                if x in f:
                    print("Playing frame", x)
                    t = self.playFrame(x)
                print("Time executed: ", time.time()-a, time.time()-b)
                time.sleep((1000/self.frameRate)*0.001)"""



    def playFrame(self, frame, timeOfFrame=0):
        #Time between keyframes in ms
        #if frame != 0:
        #    timeOfFrame = (abs(frame-self.frames[self.frames.index(frame)-1])/self.frameRate)*1000
        #    timeOfFrame = timeOfFrame - self.overlap
        #else:
        #    timeOfFrame = 0
        for bone in self.script[frame]:
            b = self.boneIDToObject(bone)
            pos = self.script[frame][bone]
            try:
                if timeOfFrame < 0:
                    timeOfFrame = 0
                b.setAngle(pos, time=timeOfFrame)
            except:
                #pass
                print("ERROR: Bone prolly jaw or tail. Skipping.", bone)

        #return timeOfFrame

    def setStartingPositions(self):
        f = self.getFrames()
        del f[0]
        s = min(self.script)
        for bone in self.script[s]:
            b = self.boneIDToObject(bone)
            pos = self.script[s][bone]
            try:
                b.setAngle(pos, time=1)
            except:
                print("ERROR: Bone prolly jaw or tail. Skipping.", bone)

    def boneIDToObject(self, boneID):
        if boneID.startswith("Leg"):
            legID = int(boneID[3])
            leg = self.hexapod.legs.getLeg(legID)
            if boneID.endswith("Tibia"):
                return leg.tibia
            elif boneID.endswith("Femur"):
                return leg.femur
            elif boneID.endswith("Coxa"):
                return leg.coxa
        elif boneID.startswith("Tail"):
            tail = self.hexapod.tail
            if boneID.endswith("Yaw"):
                return tail.yaw
            elif boneID.endswith("Pitch"):
                return tail.pitch
        elif boneID.startswith("Jaw"):
            jaw = self.hexapod.mandibles
            if boneID.endswith("Pitch"):
                return jaw.pitch
            elif boneID.endswith("Yaw"):
                return jaw.yaw
            elif boneID.endswith("Roll"):
                return jaw.roll
            elif boneID.endswith("LeftTooth"):
                return jaw.leftJaw
            elif boneID.endswith("RightTooth"):
                return jaw.rightJaw

    def startTimer(self):
        self.startingTime = time.clock()

    def getTime(self):
        return time.clock()-self.startingTime
