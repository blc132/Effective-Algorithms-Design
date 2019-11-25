from random import randint, random

import numpy
import math
from graph import Graph
from collections import deque

from helpers import INF, generate_random_number



class SimulatedAnnealing(Graph):
    route = deque()
    temperature_coefficient: float
    temperature_current: float
    temp_route: []
    final_route: []
    temp_cost: int

    def __init__(self, graph):
        Graph.__init__(self, filename="", choice=-1)

        self.cost_matrix = graph.cost_matrix
        self.file_name = graph.file_name
        self.number_of_cities = graph.number_of_cities

        self.temp_route = numpy.empty(self.number_of_cities, dtype=int)
        self.final_route = numpy.empty(self.number_of_cities, dtype=int)
        self.temperature_coefficient = 0
        self.temperature_current = 0
        self.temp_cost = 0
        self.route.clear()

    def accept_solution(self, delta_energy):
        if delta_energy < 0:
            return True
        elif random() <= math.exp(-(delta_energy/self.temperature_current)):
            return True
        return False

    def generate_probability(self):
        value = pow(math.e, (self.best_cycle_cost - self.temp_cost // self.temperature_current))
        print("value: " + str(value))
        print("e: " + str(math.e))
        print("best_cycle_cost: " + str(self.best_cycle_cost))
        print("temperature_current: " + str(self.temperature_current))

        if value < 1.0:
            return value
        return 1.0

    def generate_permutation(self):
        first_index = randint(0, self.number_of_cities - 1)

        while True:
            second_index = randint(0, self.number_of_cities - 1)
            if first_index != second_index:
                break

        aux_number = self.final_route[first_index]

        self.temp_route = self.final_route
        self.temp_route[first_index] = self.temp_route[second_index]
        self.temp_route[second_index] = aux_number

    def geometric_temperature_computation(self):
        # print(self.temperature_current)
        # print(self.temperature_coefficient)
        self.temperature_current *= self.temperature_coefficient

    def get_path_length(self, index_matrix):
        weight_of_path = 0

        for x in range(0, self.number_of_cities - 1):
            weight_of_path += self.cost_matrix[index_matrix[x], index_matrix[x + 1]]

        weight_of_path += self.cost_matrix[index_matrix[self.number_of_cities - 1], index_matrix[0]]
        return weight_of_path

    def start(self, temperature_max, temperature_min, temperature_coefficient):
        self.temperature_current = temperature_max
        self.temperature_coefficient = temperature_coefficient

        for x in range(0, self.number_of_cities):
            self.final_route[x] = x

        self.temp_route = self.final_route

        self.best_cycle_cost = self.get_path_length(self.temp_route)
        self.temp_cost = self.best_cycle_cost

        while self.temperature_current > temperature_min:
            self.generate_permutation()
            self.temp_cost = self.get_path_length(self.temp_route)

            delta = self.temp_cost - self.best_cycle_cost

            if self.accept_solution(delta):
                self.best_cycle_cost = self.temp_cost
                self.final_route = self.temp_route

            self.geometric_temperature_computation()

        for x in range(0, self.number_of_cities):
            self.route.append(self.final_route[x])
        self.route.append(self.final_route[0])

    def display_optimal_route(self):
        x = len(self.route) - 1
        route = ""
        while x >= 0:
            if x > 0:
                route += str(self.route[x]) + " -> "
            else:
                route += str(self.route[x])
            x -= 1
        print(route)
