from graph import Graph
from collections import deque

from helpers import lets_say_its_inf, ptype


class BruteForce(Graph):
    route = deque()
    aux_route = deque()
    visited = []
    starting_vertex = 0
    aux_cycle_cost = 0

    def __init__(self, graph):
        Graph.__init__(self, filename="", choice=-1)
        self.best_cycle_cost = lets_say_its_inf()

        self.neighbourhood_matrix = graph.neighbourhood_matrix
        self.cost_matrix = graph.cost_matrix
        self.file_name = graph.file_name
        self.number_of_cities = graph.number_of_cities

        self.visited = [False] * self.number_of_cities

    def start(self, current_vertex):
        self.aux_route.append(current_vertex)

        if len(self.aux_route) < self.number_of_cities:
            self.visited[current_vertex] = True

            for x in range(self.number_of_cities):
                if self.neighbourhood_matrix[current_vertex, x] and not self.visited[x]:
                    self.aux_cycle_cost += self.cost_matrix[current_vertex, x]
                    self.start(x)
                    self.aux_cycle_cost -= self.cost_matrix[current_vertex, x]
            self.visited[current_vertex] = False
        elif self.neighbourhood_matrix[self.starting_vertex, current_vertex]:
            self.aux_cycle_cost += self.cost_matrix[current_vertex, self.starting_vertex]

            if self.aux_cycle_cost < self.best_cycle_cost:
                self.route.clear()
                self.best_cycle_cost = self.aux_cycle_cost
                self.route = self.aux_route.copy()
                self.route.append(self.starting_vertex)
            self.aux_cycle_cost -= self.cost_matrix[current_vertex, self.starting_vertex]

        self.aux_route.pop()

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