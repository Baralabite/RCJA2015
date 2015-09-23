import pygame, math, time, rpyc

class Bone:
    def __init__(self, head, angle, length):
        self.head = head
        self.tail = (0,0)
        self.angle = angle
        self.length = length

        self.update()

    def update(self):
        c = self.polarToCartesian(self.angle, self.length)
        self.tail = self.head[0]+c[0], self.head[1]+c[1]
        #print(self.head, self.tail)

    """
    Returns X,Y coordinate for Angle,Length (Polar) coordinate
    """
    def polarToCartesian(self, angle, length):
        x = length * math.cos(math.radians(angle))
        y = length * math.sin(math.radians(angle))
        return (x, y)

class LegIK:
    def __init__(self, hexapod):
        self.femur = Bone((0, 200), 0, 80)
        self.tibia = Bone((80, 200), -90, 120)


        self.hexapod = hexapod

        self.alpha = 0          #Femur Angle
        self.beta = 0           #Tibia Angle
        self.gamma = 0          #Coxa Angle (Unused in this demo)        

        self.target = (200, 0)
        self.yTarget = 0

    def setTarget(self, pos):
        self.target = pos[0], pos[1]
        self.calculate()

    """
    Returns distance between two points
    """
    def distanceFormula(self, pos1, pos2):
        return math.sqrt((pos2[0]-pos1[0])**2+(pos2[1]-pos1[1])**2)

    def calculate(self):
        if True:
            self.gamma = math.degrees(math.atan(self.yTarget/200))

            #print("T:", self.target)
            self.L = self.distanceFormula(self.femur.head, self.target)
            #print("L:",self.L)

            self.a1 = math.degrees(math.acos((200-self.target[1])/self.L))
            #print("A1:",self.a1)
        try:
            self.a2 = math.degrees(math.acos(((self.tibia.length**2)-(self.femur.length**2)-(self.L**2))/(-2 * self.femur.length * self.L)))
            #print("A2:",self.a2)

            #self.a = math.degrees(math.acos(200/self.L)) + self.degrees(self.acos((200**2 - 200**2 - self.L**2)/(-2*200*self.L)))
            self.a = self.a1 + self.a2
            #print("A:",self.a)
            

            self.b = math.degrees(math.acos(((self.L**2) - (self.tibia.length**2) - (self.femur.length**2))/(-2*self.tibia.length*self.femur.length)))
            #print("B:",self.b)

            #print("D:", self.distanceFormula(self.femur.tail, self.target))

            self.femur.update()
            self.femur.angle = self.a-90
            self.tibia.head = self.femur.tail
            self.tibia.angle = (self.b-180)+self.femur.angle
            self.tibia.update()

            print(self.tibia.angle+90)

            self.hexapod.legs.getLeg(4).femur.setAngle(self.femur.angle)
            self.hexapod.legs.getLeg(4).tibia.setAngle((self.b-180)+90)
            
        except:
            pass

class Dog:
    def __init__(self):
        pass

    def __repl__(self):
        return (1, 3)
        

class Application:
    def __init__(self):
        self.surface = pygame.display.set_mode((400, 400))
        
        self.running = False

        

    def start(self):
        a = rpyc.connect("192.168.2.100", 12345)
        self.hexapod = a.root.exposed_get_app().hexapod
        self.ik = LegIK(self.hexapod)
        self.running = True
        self.loop()

    def stop(self):
        self.running = False    

    def loop(self):
        while self.running:
            self.tick()
            time.sleep(0.01)

    """
    Called every frame
    """
    def tick(self):
        self.surface.fill((0,0,0))

        self.drawIK()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.ik.setTarget(self.toNormal(event.dict["pos"]))
                
                
        
        pygame.display.flip()        

    def line(self, pos1, pos2):
        pygame.draw.line(self.surface, (255, 255, 255), self.toPygame(pos1), self.toPygame(pos2))

    def drawIK(self):        
        self.ik.calculate()
 
        pygame.draw.line(self.surface, (255, 255, 255), self.toPygame(self.ik.femur.head), self.toPygame(self.ik.femur.tail))

        pygame.draw.line(self.surface, (255, 255, 255), self.toPygame(self.ik.tibia.head), self.toPygame(self.ik.tibia.tail))

    """
    Util function. Converts coords to pygame space.
    """
    def toPygame(self, pos):
        return pos[0], 400-pos[1]

    def toNormal(self, pos):
        return pos[0], abs(400-pos[1])
        
    

if __name__ == "__main__":
    app = Application()
    app.start()
