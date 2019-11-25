import numpy

from graph.graph import Graph
from collections import deque

from helpers.helpers import INF


class DynamicProgramming(Graph):
    route = deque()
    all_visited_vertices_mask = 0
    starting_vertex = 0
    all_vertices_subsets = [int, int]
    sub_path_indexes = [int, int]

    def __init__(self, graph):
        Graph.__init__(self, filename="", choice=-1)
        self.best_cycle_cost = INF

        self.cost_matrix = graph.cost_matrix
        self.file_name = graph.file_name
        self.number_of_cities = graph.number_of_cities
        # maska bitowa wszystkich odwiedzonych miast (2^n)-1
        self.all_visited_vertices_mask = (1 << self.number_of_cities) - 1
        # dla każdego miasta oddzielna maska, czyli tablica dwuwymiarowa [n, (2^n)-1]
        self.all_vertices_subsets = numpy.full((self.number_of_cities, 1 << self.number_of_cities), INF, dtype=int)
        self.sub_path_indexes = numpy.full((self.number_of_cities, 1 << self.number_of_cities), INF, dtype=int)
        self.route.clear()

        for x in range(self.number_of_cities):
            for y in range(self.all_visited_vertices_mask + 1):
                self.all_vertices_subsets[x, y] = INF
                self.sub_path_indexes[x, y] = INF

    def start(self, starting_vertex):
        # przypisanie starowego wierzchołka
        self.starting_vertex = starting_vertex

        # dopisanie do maski bitowej startowego wierzchołka, w domyśle to po prostu 000...01
        current_state_of_vertices = 1 << starting_vertex

        self.best_cycle_cost = self.__start(starting_vertex, current_state_of_vertices)

        index = starting_vertex
        # przepisanie indeksów na ścieżkę grafu
        for x in range(self.number_of_cities):
            self.route.append(index)
            next_index = self.sub_path_indexes[index, current_state_of_vertices]
            current_state_of_vertices |= 1 << next_index
            index = next_index

        self.route.append(starting_vertex)

    def __start(self, current_vertex, current_vertex_state_mask):

        # jeśli maska == 11..11, zwróć koszt pomiędzy aktualnym wierzchołkiem a pierwszym
        if current_vertex_state_mask == self.all_visited_vertices_mask:
            return self.cost_matrix[current_vertex, self.starting_vertex]

        # jeśli maska została wczeniej obliczona to zwróć ją
        if self.all_vertices_subsets[current_vertex, current_vertex_state_mask] != INF:
            return self.all_vertices_subsets[current_vertex, current_vertex_state_mask]

        minimum_cost_of_travel = INF
        current_vertex_index: int = -1

        for x in range(self.number_of_cities):
            # jesli zostalo odwiedzone, czyli AND == 1
            if current_vertex_state_mask & (1 << x) != 0:
                continue
            # kolejna maska to będzie aktualna OR maska startowa wierzchołka x
            next_state_mask = current_vertex_state_mask | (1 << x)
            new_cost_of_travel = self.cost_matrix[current_vertex, x] + self.__start(x, next_state_mask)

            if new_cost_of_travel < minimum_cost_of_travel:
                minimum_cost_of_travel = new_cost_of_travel
                current_vertex_index = x

        self.sub_path_indexes[current_vertex, current_vertex_state_mask] = current_vertex_index
        self.all_vertices_subsets[current_vertex, current_vertex_state_mask] = minimum_cost_of_travel

        return self.all_vertices_subsets[current_vertex, current_vertex_state_mask]

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
