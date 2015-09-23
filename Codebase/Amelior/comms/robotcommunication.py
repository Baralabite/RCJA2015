import socket, logging
from Amelior.config.config import *

class RobotCommunication:
    def __init__(self):
        self.host = None
        self.logger = logging.getLogger(Config.LOGGING_NAME+".Hexapod")

    def connect(self, host):
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.host)
        except:
            print(host)
            self.logger.error("Connection failed!")
            quit()

    def poll(self):
        pass

    def send(self, data):
        self.socket.send(data)

    def close(self):
        self.socket.close()