import os, logging, base64
from Amelior.config.config import Config
import Amelior

class ConfigParser:
    """
    Model is the hexapod model to get config from (e.g. BaralabaBob/LynxmotionAPod)
    """
    def __init__(self, model):
        self.model = model
        self.root = os.path.join(os.path.dirname(Amelior.__file__), "config/model/"+self.model)
        self.logger = logging.getLogger(Config.LOGGING_NAME+".ConfigParser")

        self.wasBase64 = False

    """
    path: Path where the desired config file resides.
    """
    def loadConfig(self, path):
        self.logger.debug("Loading config "+path)
        try:
            return eval(open(os.path.join(self.root, path), "r").read())
        except:
            try:
                data = eval(base64.b64decode(bytes(open(f, "r").read())).decode("utf-8"))
                self.debug("Loaded config. It was encoded in base64.")
                self.wasBase64 = True
                return data
            except:
                self.logger.error("Failed to parse "+path+".")


    """
    path: file in which to save it
    data: dictionary to save
    """
    def saveConfig(self, path, data):
        self.logger.debug("Saving config to "+path)
        f = open(os.path.join(self.root, path), "w")
        f.write(str(data))

    """
    Returns True if the last file loadConfig loaded was encoded with base64.
    """
    def wasBase64(self):
        return self.wasBase64