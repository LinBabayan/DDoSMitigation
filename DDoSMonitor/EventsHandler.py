from enum import Enum, auto

class EventName(Enum):
    PARSED_DATA_AVAILABLE = auto()
    DDOS_ATTACK_DETECTED = auto()
    TRAINING_MODEL_FINISHED = auto()

class EventsHandler(object):
    def __init__(self):
        self._subscribers = {}
        for event in EventName:
            self._subscribers[event] = []

    def subscribe(self, event_name, callback):
        self._subscribers[event_name].append(callback)

    def publish(self, event_name, data):
        for callback in self._subscribers[event_name]:
            callback(data)

# Singleton instance
events_handler = EventsHandler()


