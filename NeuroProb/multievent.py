import numpy as np

END = 0
ACTIVATE = 1
DEACTIVATE = 2

class Multievent:
    def __init__(self, events, times):
        assert len(events) == len(times), "Number of events must match number of times"
        self.events = events
        self.times = times
        self.sort()

    def sort(self):
        order = np.argsort(self.times)
        self.events = self.events[order]
        self.times = self.times[order]