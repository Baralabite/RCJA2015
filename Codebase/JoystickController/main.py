import pygame, rpyc, threading

class Application:
    def __init__(self):
        self.running = False

        """
        Resolution of the window. Because I'm not doing much with it, keep it small.
        """
        self.screen_resolution = (200, 200)

        """
        Surface to clear and blit to in pygame.
        """
        self.surface = None

        """
        Address of the remote rpyc server
        """
        self.rpyc_host = ("192.168.2.100", 12345)

        """
        Variable to store rpyc connection instance
        """
        self.rpyc_connection = None

        """
        Remote hexapod object. Remote object handled by rpyc.
        """
        self.hexapod = None

        """
        Joystick object
        """
        self.joystick = None

        """
        Operational flags
        """
        self.stepping = False

    """
    Called to create the window, connect to the hexapod, and init the joystick
    """
    def start(self):
        #Create the surface
        self.surface = pygame.display.set_mode(self.screen_resolution)

        #Connects to remote, and gets the hexapod object.
        self.rpyc_connection = rpyc.connect(self.rpyc_host[0], self.rpyc_host[1])
        self.hexapod = self.rpyc_connection.root.exposed_get_app().hexapod
        print(self.hexapod)

        #Inits the joystick
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        #Starts the loop.
        self.running = True
        self.loop()

    """
    Called to close everything down.
    On the next "pass" of the loop in self.loop, it exits, because self.running != True
    """
    def stop(self):
        self.rpyc_connection.close()
        pygame.joystick.quit()
        pygame.quit()
        self.running = False

    def loop(self):
        #Operational flags
        hexapodOn = False
        stepping = False
        while self.running:
            self.surface.fill((0, 0, 0))


            #Handle events here:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        if hexapodOn:
                            #self.hexapod.turnOff()
                            self.hexapod.turnOn()
                            hexapodOn = False
                        else:
                            self.hexapod.turnOn()
                            hexapodOn = True

                if event.type == pygame.JOYAXISMOTION and event.axis in [0, 1]:
                    if event.value > 0.3 or event.value < 0.3:
                        x, y = self.joystick.get_axis(0)*15, self.joystick.get_axis(1)*15*-1
                        print(self.joystick.get_axis(0), self.joystick.get_axis(1)*-1)
                        print("Moving to:",(x, y))
                        self.hexapod.step((x, y))

                #print(event.dict)


            pygame.display.flip()
        print("Bye!")
        quit()

    def stepFinishedCallback(self):
        self.stepping = False
        print("Calledback!")

if __name__ == "__main__":
    app = Application()
    app.start()