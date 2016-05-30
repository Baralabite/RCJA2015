import sys, rpyc
sys.dont_write_bytecode = True
sys.path.append("/home/pi/BaralabaBob/Codebase")

from model import hexapod
from config.config import *
from code import InteractiveConsole
from os import path
from threading import Thread
import logging, datetime, time
from Amelior.util.scriptexecutor import ScriptExecutor
from Amelior.util.position3d import Position3D
from Amelior.util.action import Action

class Application():
    def __init__(self):
        self.initLogging()
        self.logger.info("BaralabaBob Hexapod Server")

        self.cached = False

        self.routineRunning = False

    """
    Sets up the logging
    """
    def initLogging(self):
        self.logger = logging.getLogger(Config.LOGGING_NAME)
        self.logger.setLevel(logging.DEBUG)

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')# %H.%M.%S')
        fh = logging.FileHandler(path.join(path.dirname(__file__), "logs/%s.txt"%st))
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter("%(created)f %(thread)d %(filename)s,%(lineno)d %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        #self.logger.addHandler(ch)

    """
    Runs the console thread.
    """
    def start(self):
        self.logger.info("Initializing Hexapod...")
        self.hexapod = hexapod.Hexapod()

        self.se = ScriptExecutor(self.hexapod)

        self.logger.info("Starting RPyC server...")
        self.rpycServerThread = Thread(target=self.runRPyCServer)
        self.rpycServerThread.setDaemon(True)
        self.rpycServerThread.start()

        self.logger.debug("Starting interactive shell thread...")
        self.consoleThread = Thread(target=self.startInteractiveShell)
        self.consoleThread.start()

    def runRPyCServer(self):
        rpyc.core.protocol.DEFAULT_CONFIG['allow_setattr'] = True
        rpyc.core.protocol.DEFAULT_CONFIG['allow_all_attrs'] = True
        from rpyc.utils.server import ThreadedServer
        self.rpycServer = ThreadedServer(RPyCService, port = 12345)
        self.rpycServer.start()

    """
    Starts a local interactive shell
    Threaded
    """
    def startInteractiveShell(self):
        vars = globals()

        l1 = self.hexapod.legs.getLeg(1)
        l2 = self.hexapod.legs.getLeg(2)
        l3 = self.hexapod.legs.getLeg(3)
        l4 = self.hexapod.legs.getLeg(4)
        l5 = self.hexapod.legs.getLeg(5)
        l6 = self.hexapod.legs.getLeg(6)
        h = self.hexapod

        vars.update(locals())
        shell = InteractiveConsole(vars)
        shell.interact()

    def cacheRoutine(self):
        if not self.cached:
            self.createDestroy = Action("createDestroy", self.hexapod)
            self.clocks = Action("clocks", self.hexapod)
            self.beatIt = Action("beatIt", self.hexapod)
            self.allByMyself = Action("allByMyself", self.hexapod)
            self.lionKing = Action("circleOfLife", self.hexapod)
            self.cached = True

    """
    Routines are temporarily stored here.
    """
    def rcjaRoutine(self):
        self.routineRunning = True
        time.sleep(1.6)
        if not self.routineRunning:
            self.hexapod.turnOn()
            return
        self.createDestroy.repeatAction(1)
        if not self.routineRunning:
            self.hexapod.turnOn()
            return
        self.clocks.repeatAction(1)
        if not self.routineRunning:
            self.hexapod.turnOn()
            return
        self.beatIt.repeatAction(1)
        if not self.routineRunning:
            self.hexapod.turnOn()
            return
        self.allByMyself.repeatAction(1)
        if not self.routineRunning:
            self.hexapod.turnOn()
            return
        self.lionKing.repeatAction(1)
        if not self.routineRunning:
            self.hexapod.turnOn()
            return

        """self.se.playAction("createDestroy")
        self.se.playAction("clocks")
        self.se.playAction("beatIt")
        self.se.playAction("allByMyself")"""

    def rcjaStateRoutine(self):
        time.sleep(15.6)
        self.se.playAction("CarminiaBurana")
        time.sleep(1.5)
        self.se.playAction("Beegees")
        time.sleep(0.03)
        self.se.playAction("BadSongs")
        self.se.playAction("PinkPanther")
        time.sleep(0.6)
        self.se.playAction("iFeelGood")


class RPyCService(rpyc.Service):
    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalzize the service, if needed)
        pass

    def exposed_get_app(self): # this is an exposed method
        return app

    def exposed_get(self):
        return app.se

    def exposed_move(self, case):
        if case == 0:
            app.se.playAction("walkForward_")
        elif case == 1:
            app.se.playAction("walkBackward_")
        elif case == 2:
            app.se.playAction("walkLeft_")
        elif case == 3:
            app.se.playAction("walkRight_")
        elif case == 4:
            app.se.playAction("turnLeft_")
        elif case == 5:
            app.se.playAction("turnRight_")


    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"



#If run as a standalone program, it starts up as a server.
#When doing this, remote mode is not avaliable!
if __name__ == "__main__":
    logging.info("WARNING: Running as a standalone program means that you cannot remotely access it!")
    app = Application()
    app.start()

