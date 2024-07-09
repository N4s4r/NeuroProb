import numpy as np

END = 0
ACTIVATE = 1
DEACTIVATE = 2

class Multievent:
    def __init__(self, events=[], times=[], regions=[]):
        assert len(events) == len(times), "Number of events must match number of times"
        self.events = np.array(events, dtype=int)
        self.times = np.array(times, dtype=float)
        self.regions = np.array(regions, dtype=int)
        self.sort()

    def sort(self):
        order = np.argsort(self.times)
        self.events = self.events[order]
        self.times = self.times[order]
        self.regions = self.regions[order]

    def add_event(self, event, time, region):
        self.events = np.append(self.events, event)
        self.times = np.append(self.times, time)
        self.regions = np.append(self.regions, region)
        self.sort()
    
    def __str__(self):
        string = ""
        for event, time, region in zip(self.events, self.times, self.regions):
            string += f"{time:.2f}: {event} {region}\n"
        return string
