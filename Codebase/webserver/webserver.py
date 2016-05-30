from bottle import route, run, template, static_file, request
import rpyc, threading

conn = rpyc.connect("localhost", 12345)
app = conn.root.exposed_get_app()
hexapod = app.hexapod

repeatingFunction = None

@route('/')
def index():
    app.cacheRoutine()
    return static_file("index.html", root='/home/pi/BaralabaBob/Codebase/webserver/templates')

@route('/turn_on')
def action():
    if app.hexapod.on:
        app.hexapod.turnOff()
    else:
        app.hexapod.turnOn()

@route('/api/<command>')
def api(command):
    global repeatingFunction

    if command == "toggleOn":
        if app.hexapod.on:
            repeatingFunction = lambda: app.hexapod.turnOff()
        else:
            repeatingFunction = lambda: app.hexapod.turnOn()

    elif command == "walkForward":
        repeatingFunction = lambda: app.se.playAction("walkForward_")

    elif command == "turnLeft":
        repeatingFunction = lambda: app.se.playAction("turnLeft_")

    elif command == "turnRight":
        repeatingFunction = lambda: app.se.playAction("turnRight_")

    elif command == "dance":
        repeatingFunction = lambda: None
        routineThread = threading.Thread(target=app.rcjaRoutine)
        routineThread.setDaemon(True)
        routineThread.start()

    elif command == "stopRoutine":
        app.routineRunning = False
        repeatingFunction = lambda: None


    elif command == "stop":
        repeatingFunction = lambda: None

running = True
def runCommand():
    while running:
        if repeatingFunction:
            repeatingFunction()


@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='/home/pi/BaralabaBob/Codebase/webserver/templates')

thread = threading.Thread(target=runCommand)
thread.setDaemon(True)
thread.start()
run(host='0.0.0.0', port=8080)