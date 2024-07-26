import numpy as np
import matplotlib.pyplot as plt

END = 0
ACTIVATE = 1
DEACTIVATE = 2

def event_code_to_string(event):
    if event == END:
        return "END"
    if event == ACTIVATE:
        return "ACTIVATE"
    if event == DEACTIVATE:
        return "DEACTIVATE"
    return "UNKNOWN"

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
    
    def plot(self, region_names):
        self.sort()
        # Check that the simulation ends
        assert self.events[-1] == END, "Simulation must end"


        # Create a figure
        fig, ax = plt.subplots(figsize=(10, 5))

        # Get the end time
        end_time = self.times[-1]

        for channel in range(len(region_names)):
            # Get the events for the channel
            channel_events = self.events[self.regions == channel]
            channel_times = self.times[self.regions == channel]
            channel_events = np.append(channel_events, END)
            channel_times = np.append(channel_times, end_time)

            # Plot the channel
            ax.plot([0, end_time],[channel, channel], "k-", label=region_names[channel])

            # For each ACTIVATE-DEACTIVATE pair, plot a rectangle
            for i in range(1, len(channel_events), 2):
                start = channel_times[i-1]
                end = channel_times[i]
                ax.fill_between([start, end], [channel-0.45, channel-0.45], [channel+0.45, channel+0.45], color="blue", alpha=0.5)
        
        # Set the channel names
        ax.set_yticks(range(len(region_names)))
        ax.set_yticklabels(region_names)
        plt.show()
    
    def __str__(self):
        string = ""
        for event, time, region in zip(self.events, self.times, self.regions):
            string += f"{time:.2f}: {event_code_to_string(event)} {region}\n"
        return string
