import threading, inspect, urllib.request, BaralabaBob
from os.path import *
import imp
#
#from BaralabaBob.util.sequenceexecutor import *;
# se = SequenceExecutor(self.hexapod, "C:\Python34\Lib\site-packages\BaralabaBob\config\model\BaralabaBob\scripts\\tailShake.cfg", repeat=10).runSequence()


class SequenceExecutor:
    def __init__(self):
        self.configDir = join(dirname(BaralabaBob.__file__), "config\model\BaralabaBob\scripts")



    def getScript(self, name, remote=None):
        if remote:
            urllib.request.urlretrieve(remote, join(self.configDir, name+".py"))
            urllib.request.urlcleanup()

        namespace = {}
        exec("from BaralabaBob.config.model.BaralabaBob.scripts import {}".format(name), globals(), namespace)
        exec("scripts = [obj for name,obj in inspect.getmembers({}) if inspect.isclass(obj)]".format(name), globals(), namespace)
        return namespace["scripts"][0]


