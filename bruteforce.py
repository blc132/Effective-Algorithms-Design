from graph import Graph
from collections import deque

from helpers import INF


class BruteForce(Graph):
    route = deque()
    aux_route = deque()
    visited = []
    starting_vertex = 0
    aux_cycle_cost = 0

    def __init__(self, graph):
        Graph.__init__(self, filename="", choice=-1)
        self.best_cycle_cost = INF

        self.cost_matrix = graph.cost_matrix
        self.file_name = graph.file_name
        self.number_of_cities = graph.number_of_cities

        self.visited = [False] * self.number_of_cities

    def start(self, current_vertex):
        self.aux_route.append(current_vertex)

        # jesli route jest mniejszy to zaznacz ten wierzchołek jako odwiedzony
        # w przeciwnym razie to oznacza, ze zrobilismy caly cykl hamiltona i ten wierzcholek byl juz odwiedzony
        if len(self.aux_route) < self.number_of_cities:
            self.visited[current_vertex] = True

            for x in range(self.number_of_cities):
                # jesli wierzcholki current_vertex i x są sąsiadami i wierzchołek x nie był odwiedzony
                if not self.visited[x]:
                    # dodaj do tymczasowego kosztu koszt pomiedzy current_vertex i x
                    self.aux_cycle_cost += self.cost_matrix[current_vertex, x]
                    # i zacznij metode od wierzcholka x
                    self.start(x)
                    # usuwamy koszt który był w poprzedniej iteracji
                    self.aux_cycle_cost -= self.cost_matrix[current_vertex, x]
            self.visited[current_vertex] = False
        # jesli to ostatni cykl, tj. zostala trasa od ostatniego do pierwszego
        else:
            self.aux_cycle_cost += self.cost_matrix[current_vertex, self.starting_vertex]

            # sprawdzenie czy tymczasowy koszt jest lepszy (tj. mniejszy) niz aktualnie najlepszy koszt
            if self.aux_cycle_cost < self.best_cycle_cost:
                self.route.clear()
                self.best_cycle_cost = self.aux_cycle_cost
                self.route = self.aux_route.copy()
                self.route.append(self.starting_vertex)
            # usuwamy koszt który był w poprzedniej trasie
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
