import os
import numpy


def parse_int(s, base=10, val=False):
    if s.isdigit():
        return int(s, base)
    else:
        return val


class Graph:
    number_of_cities = int
    cost_matrix = [int, int]
    neighbourhood_matrix = [bool, bool]
    best_cycle_cost = int
    all_numbers = []
    absolute_directory = ""
    x_position = int
    y_position = int
    end_parsing_from_file = bool
    started_parsing_numbers = bool
    file_name = ""

    # def __init__(self):
    # self.number_of_citites = int
    # self.cost_matrix = [int, int]
    # self.neighbourhood_matrix = [bool, bool]
    # self.best_cycle_cost = int
    # self.all_numbers = []
    # self.absolute_directory
    # self.x_position = int
    # self.y_position = int
    # self.end_parsing_from_file = bool
    # self.started_parsing_numbers = bool
    # self.file_name

    def __init__(self, filename, choice):
        self.best_cycle_cost = float("inf")
        self.file_name = filename
        self.x_position = 0
        self.y_position = 0
        self.end_parsing_from_file = False
        self.absolute_directory = os.path.dirname(os.path.realpath(__file__)) + "\\Macierze PEA\\"

    def parse_small_graph(self, absolute_directory, file_name):
        absolute_directory = absolute_directory + "small\\" + file_name
        separators = {' ', '\r'}

        try:
            self.all_text = open(absolute_directory, 'r')
            self.all_numbers = self.all_text.split(separators)
            if self.all_numbers is None:
                raise Exception("Taki plik nie istnieje!")

            self.number_of_cities = int(self.all_numbers[0])
            self.neighbourhood_matrix = numpy.zeros((self.number_of_cities, self.number_of_cities), dtype=bool)
            self.cost_matrix = numpy.zeros((self.number_of_cities, self.number_of_cities), dtype=int)
            self.create_cost_matrix()
            self.set_infinity_on_inaccessible_places()
            self.create_neighbourhood_matrix()
        except Exception:
            print(Exception + "\n")

    def parse_large_graph(self, absolute_directory, file_name):
        absolute_directory = absolute_directory + "large\\" + file_name
        parsed_number_of_cities = False

        try:
            with open(absolute_directory, "r") as file:
                for line in file:
                    line_text_array = line.split(' ')
                    if not parsed_number_of_cities:
                        try_to_parse = self.try_parse_number_of_cities(line_text_array)
                        if try_to_parse:
                            self.neighbourhood_matrix = numpy.zeros((self.number_of_cities, self.number_of_cities), dtype=bool)
                            self.cost_matrix = numpy.zeros((self.number_of_cities, self.number_of_cities), dtype=int)
                            parsed_number_of_cities = True
                    if parsed_number_of_cities:
                        self.parse_numbers_to_matrix(line_text_array)
                    if self.end_parsing_from_file:
                        break
        except Exception:
            print(Exception + "\n")


    def set_infinity_on_inaccessible_places(self):
        for x in range(self.number_of_cities):
            self.cost_matrix[x, x] = float("inf")

    def try_parse_number_of_cities(self, line_text_array):
        success = False
        for word in line_text_array:
            if "DIMENSION:" in word:
                success = True
            if success:
                number_of_cities = parse_int(word)
                if number_of_cities:
                    return True
        return False

    def parse_numbers_to_matrix(self, line_text_array):
        for word in line_text_array:
            if "EDGE_WEIGHT_SECTION" in word:
                self.started_parsing_numbers = True
            if self.started_parsing_numbers:
                success = parse_int(word)
                if success:
                    self.cost_matrix[self.x_position, self.y_position] = success
                    if self.x_position < self.number_of_cities - 1:
                        self.x_position += 1
                    else:
                        self.x_position = 0
                        self.y_position += 1
            if self.x_position == self.number_of_cities - 1 & self.y_position == self.number_of_cities - 1:
                self.end_parsing_from_file = True

    def create_cost_matrix(self):
        success = False
        aux = 1
        x = 0
        y = 0
        while x < self.number_of_cities:
            while y < self.number_of_cities:
                success = parse_int(self.all_numbers[aux])
                if success:
                    y += 1
                    self.cost_matrix[x, y] = success
            if success:
                x += 1

    def create_neighbourhood_matrix(self):
        for x in range(self.number_of_cities):
            for y in range(self.number_of_cities):
                if self.cost_matrix[x, y] != float("inf"):
                    self.neighbourhood_matrix[x, y] = True
                else:
                    self.neighbourhood_matrix[x, y] = False

    def display_cost_matrix(self):
        for x in range(self.number_of_cities):
            for y in range(self.number_of_cities):
                if self.cost_matrix[x, y] == float("inf"):
                    print("0 ")
                else:
                    print(self.cost_matrix[x, y] + " ")
            print("\n")

    def display_neighbourhood_matrix(self):
        for x in range(self.number_of_cities):
            for y in range(self.number_of_cities):
                if self.neighbourhood_matrix[x, y]:
                    print("1 ")
                else:
                    print("0 ")
            print("\n")
