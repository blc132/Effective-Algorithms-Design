from random import randint

import numpy
import math
from graph import Graph
from collections import deque

from helpers import INF


class SimulatedAnnealing(Graph):
    route = deque()
    temperature_coefficient: float
    temperature_current: float
    temp_route: []
    final_route: []

    def __init__(self, graph):
        Graph.__init__(self, filename="", choice=-1)
        self.temp_route = int[self.number_of_cities]
        self.final_route = int[self.number_of_cities]
        self.temperature_coefficient = 0
        self.temperature_current = 0;

    def generate_probability(self, a, b):
        probability_from_equation = math.pow(math.e, (-1 * (b - a)) / self.temperature_current)
        normal_probability = randint()

        if normal_probability < probability_from_equation:
            return 1
        return 0

    def generate_permutation(self, array_of_indexes):

        aux_matrix = int[self.number_of_cities]

        for x in range(self.number_of_cities, 0, -1):
            random_index = randint() % x
            array_of_indexes[x - 1] = aux_matrix[random_index]
            aux_matrix = aux_matrix[x - 1]

    def arithmetic_temperature_computation(self):
        self.temperature_current -= self.temperature_coefficient

    def geometric_temperature_computation(self):
        self.temperature_current *= self.temperature_coefficient

    def get_path_length(self, index_matrix):
        weight_of_path: int

        for x in range(self.number_of_cities, 0, -1):
            weight_of_path += self.cost_matrix[index_matrix[x], index_matrix[0]]

        weight_of_path += self.cost_matrix[index_matrix[self.number_of_cities - 1], index_matrix[0]]

        return weight_of_path

    def start_sa(self, temperature_max, temperature_min, temperature_coefficient):
        global first_index
        first_index: int
        second_index: int
        a: int
        b: int
        temporary_difference = 0
        difference = 0
        self.temperature_current = temperature_coefficient

        for x in range(0, self.number_of_cities):
            self.generate_permutation(self.final_route)
            self.generate_permutation(self.temp_route)

            temporary_difference = abs(self.get_path_length(self.final_route) - self.get_path_length(self.temp_route))

            if temporary_difference > difference:
                difference = temporary_difference

        self.temperature_current = difference

        self.generate_permutation(self.final_route)
        a = self.get_path_length(self.final_route)
        self.final_route = self.temp_route

        while self.temperature_current > temperature_min:
            first_index = randint() % self.number_of_cities

        while True:
            second_index = randint() % self.number_of_cities
            if second_index != first_index:
                break

        self.temp_route[second_index] = self.final_route[first_index]
        self.temp_route[first_index] = self.final_route[second_index]

        b = self.get_path_length(self.temp_route)

        if b <= a | self.generate_probability(a, b) == 1:
            a = b

            if a <= self.best_cycle_cost:
                self.best_cycle_cost = a
                self.route.clear()

                for x in range(0, self.number_of_cities):
                    self.route.append([x])
                self.route.append(self.temp_route[0])

            self.final_route[first_index] = self.temp_route[first_index]
            self.final_route[second_index] = self.temp_route[second_index]

        else:
            self.temp_route[first_index] = self.final_route[first_index]
            self.temp_route[second_index] = self.final_route[second_index]

        self.geometric_temperature_computation()



