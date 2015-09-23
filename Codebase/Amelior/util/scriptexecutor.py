import base64, threading, time, os, Amelior
from Amelior.util.action import Action

class ScriptExecutor:
    def __init__(self, hexapod):
        self.hexapod = hexapod

    def playAction(self, action, reps=1, speed=100, overlap=0):
        action = Action(action, self.hexapod)
        #return action
        #action.setStartingPositions()
        action.overlap = overlap
        action.repeatAction(reps, speed=speed)