import logging

class EventHandler:
    listeners = {}
    logger = logging.getLogger("BaralabaBob"+".EventHandler")

    def addListener(name, event, callback):
        if not event in EventHandler.listeners: EventHandler.listeners[event] = {}

        EventHandler.listeners[event][name] = callback

    def callEvent(event, data):
        #EventHandler.logger.debug("Event %s: %s", event, config)
        if not event in EventHandler.listeners: EventHandler.listeners[event] = {}

        for listener in EventHandler.listeners[event]:
            EventHandler.listeners[event][listener](data)