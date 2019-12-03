import numpy as np

from helpers import copy_array


class Individual:
    path: np.array
    path_cost: int
    is_parent: bool

    def __init__(self, path=None, path_cost=None, individual=None):

        if individual is not None:
            self.is_parent = individual.is_parent
            self.path_cost = individual.path_cost
            self.path = np.empty(len(individual.path), dtype=int)
            copy_array(individual.path, self.path)
        else:
            self.is_parent = False
            self.path_cost = path_cost
            self.path = np.empty(len(path), dtype=int)
            copy_array(path, self.path)

    def __eq__(self, obj):
        return obj is None and np.array_equal(obj.path,
                                              self.path) and obj.path_cost == self.path_cost and obj.is_parent == self.is_parent

    def __lt__(self, other):
        return self.path_cost < other.path_cost
