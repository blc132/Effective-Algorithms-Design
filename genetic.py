import random

import numpy
from graph import Graph
from collections import deque

from individual import Individual


class Genetic(Graph):
    route = deque()
    size_of_population: int
    mutation_probability: float
    cross_probability: float
    number_of_generations: int
    population: []

    def __init__(self, graph):
        Graph.__init__(self, filename="", choice=-1)

        self.cost_matrix = graph.cost_matrix
        self.file_name = graph.file_name
        self.number_of_cities = graph.number_of_cities
        self.final_route = numpy.empty(self.number_of_cities, dtype=int)
        self.route.clear()
        self.population = []

    def start(self, number_of_generations, size_of_population, cross_probability, mutation_probability):
        self.size_of_population = size_of_population
        self.cross_probability = cross_probability
        self.mutation_probability = mutation_probability
        self.create_population()
        self.number_of_generations = 0
        number_of_childs_to_born = 50

        #pętla główna algorytmu
        while self.number_of_generations <= number_of_generations:
            for x in range(number_of_childs_to_born):
                while True:
                    first_parent = Individual(individual=self.population[random.randint(0, len(self.population) - 1)])
                    second_parent = Individual(individual=self.population[random.randint(0, len(self.population) - 1)])
                    if not (first_parent == second_parent and first_parent.is_parent and second_parent.is_parent):
                        break

                temp_rand = random.uniform(0, 1)
                if self.cross_probability >= temp_rand:

                    child = Individual(individual=self.pmx_child_creation(first_parent, second_parent))
                    self.population.append(child)

            for x in range(len(self.population)):
                self.population[x].is_parent = True

            temp_rand = random.uniform(0, 1)
            if self.mutation_probability >= temp_rand:
                individual_to_mutate = self.population[random.randint(0, len(self.population) - 1)]
                self.mutate(individual_to_mutate)

            self.population_selection()
            self.number_of_generations += 1

        best_individual = self.population[0]

        for x in range(self.number_of_cities):
            self.route.append(best_individual.path[x])
        self.best_cycle_cost = best_individual.path_cost

    def create_population(self):
        aux_individual = numpy.empty(self.number_of_cities, dtype=int)

        for x in range(self.number_of_cities):
            aux_individual[x] = x

        for x in range(self.size_of_population):
            number_of_indexes = self.number_of_cities

            while number_of_indexes > 1:
                number_of_indexes -= 1
                generated_index = random.randint(0, number_of_indexes)
                number = aux_individual[generated_index]
                aux_individual[generated_index] = aux_individual[number_of_indexes]
                aux_individual[number_of_indexes] = number

            aux_cost = self.get_path_length(aux_individual)
            individual = Individual(path=aux_individual, path_cost=aux_cost)
            individual.is_parent = True
            self.population.append(individual)

        self.population_selection()

    def mutate(self, individual):
        first_index = random.randint(0, self.number_of_cities - 1)
        second_index = random.randint(0, self.number_of_cities - 1)

        while first_index == second_index:
            second_index = random.randint(0, self.number_of_cities - 1)

        aux_number = individual.path[first_index]
        individual.path[first_index] = individual.path[second_index]
        individual.path[second_index] = aux_number
        individual.path_cost = self.get_path_length(individual.path)

    def pmx_child_creation(self, first_parent, second_parent):
        visited_cities = numpy.full(self.number_of_cities, False, dtype=bool)
        path_for_children = numpy.empty(self.number_of_cities, dtype=int)

        parent_choice = random.randint(1, 2)

        first_index_of_cut_point = random.randint(0, self.number_of_cities - 1)
        while self.number_of_cities - first_index_of_cut_point <= 2:
            first_index_of_cut_point = random.randint(0, self.number_of_cities - 1)

        second_index_of_cut_point = random.randint(first_index_of_cut_point, self.number_of_cities - 1)
        first_iterator = first_index_of_cut_point
        second_iterator = second_index_of_cut_point - first_index_of_cut_point

        if parent_choice == 1:
            for x in range(second_index_of_cut_point - first_index_of_cut_point):
                visited_cities[first_parent.path[first_iterator]] = True
                path_for_children[x] = first_parent.path[first_iterator]
                first_iterator += 1

            for x in range(self.number_of_cities):
                if not visited_cities[second_parent.path[x]]:
                    visited_cities[second_parent.path[x]] = True
                    path_for_children[second_iterator] = second_parent.path[x]
                    second_iterator += 1
        else:
            for x in range(second_index_of_cut_point - first_index_of_cut_point):
                visited_cities[second_parent.path[first_iterator]] = True
                path_for_children[x] = second_parent.path[first_iterator]
                first_iterator += 1

            for x in range(self.number_of_cities):
                if not visited_cities[first_parent.path[x]]:
                    visited_cities[first_parent.path[x]] = True
                    path_for_children[second_iterator] = first_parent.path[x]
                    second_iterator += 1

        cost_of_childs_path = self.get_path_length(path_for_children)
        return Individual(path=path_for_children, path_cost=cost_of_childs_path)

    #metoda do selekcji osobników
    def population_selection(self):
        #posortuj po długości ścieżki
        self.population.sort()

        #usuwaj ostatnich osobników tak długo aż rozmiar populacji będzie dobry
        while len(self.population) > self.size_of_population * 0.95:
            self.population.pop()

    def get_path_length(self, index_matrix):
        weight_of_path = 0

        for x in range(0, self.number_of_cities - 1):
            weight_of_path += self.cost_matrix[index_matrix[x], index_matrix[x + 1]]

        weight_of_path += self.cost_matrix[index_matrix[self.number_of_cities - 1], index_matrix[0]]
        return weight_of_path

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
