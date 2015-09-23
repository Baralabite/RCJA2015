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

class Application():
    def __init__(self):
        self.initLogging()
        self.logger.info("BaralabaBob Hexapod Server")

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

    """
    Routines are temporarily stored here.
    """
    def rcjaRoutine(self):
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
        # (to finalize the service, if needed)
        pass

    def exposed_get_app(self): # this is an exposed method
        return app

    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"



#If run as a standalone program, it starts up as a server.
#When doing this, remote mode is not avaliable!
if __name__ == "__main__":
    logging.info("WARNING: Running as a standalone program means that you cannot remotely access it!")
    app = Application()
    app.start()

