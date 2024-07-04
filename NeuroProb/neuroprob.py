import numpy as np

import utils

class NeuroProb:
    def __init__(self, connectivity, **args):
        # Assert connectivity is a square matrix
        assert connectivity.ndim == 2, "Connectivity matrix must be a 2D array"
        assert connectivity.shape[0] == connectivity.shape[1], "Connectivity matrix must be square"

        self.num_regions = connectivity.shape[0]
        self.connectivity = connectivity

        # Set the state vector
        self.state = np.zeros(self.num_regions)

        # Set region names
        self.set_region_names(**args)

        # Set baseline excitability
        self.set_excitability(**args)
    
    def set_region_names(self, region_names=None):
        if region_names is None:
            region_names = [f"CH-{i}" for i in range(self.num_regions)]
        assert len(region_names) == self.num_regions, "Number of region names must match number of regions"
        self.region_names = region_names
    
    def set_excitability(self, baseline_excitability=None, cross_excitability=None):
        if baseline_excitability is None:
            baseline_excitability = np.ones(self.num_regions)
        if cross_excitability is None:
            cross_excitability = np.ones(self.num_regions)
        assert len(baseline_excitability) == self.num_regions, "Number of baseline excitabilities must match number of regions"
        assert len(cross_excitability) == self.num_regions, "Number of cross excitabilities must match number of regions"
        self.baseline_excitability = baseline_excitability
        self.cross_excitability = cross_excitability
        self.update_excitability()
    
    def update_excitability(self):
        self.excitability = self.baseline_excitability + self.cross_excitability * np.dot(self.connectivity, self.state)
    
    # TODO: Class for the events
    def simulate(self, duration=np.inf):
        time = 0
        event = np.ones(self.num_regions) * np.inf
        while True:
            # Stop the simulation if all regions are in the seizure state
            if np.all(self.state == 1):
                break
            # For each nonseizure region, sample its time
            tau = utils.exponential_sample(self.excitability)
            # Set to infinity the time for seizure regions
            tau[self.state == 1] = np.inf
            # Find the region with the smallest time
            min_region = np.argmin(tau)
            # Update the time
            time += tau[min_region]
            # Stop the simulation if the time exceeds the duration
            if time > duration:
                break
            # Update the state of the region
            self.state[min_region] = 1
            # Update the event
            event[min_region] = time
            # Update the excitability
            self.update_excitability()
        return event
            
    

neuroprob = NeuroProb(np.random.rand(5, 5))
print(neuroprob.simulate(1))
