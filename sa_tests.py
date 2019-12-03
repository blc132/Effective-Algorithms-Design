from os import listdir, path
from os.path import isfile, join
import sys

from timeit import default_timer as timer
from graph import Graph
from main import print_to_continue
from simulatedannealing import SimulatedAnnealing


def get_script_path():
    return path.dirname(path.realpath(sys.argv[0]))

# temperature_coefficients = {
#     0.9,
#     0.99,
# }
#
# temperature_maximums = [
#     1000,
# ]
#
# temperature_minimums = [
#     0.0001
# ]

# path = "./matrixes/large"


def test(repeats, temperature_coefficients, temperature_maximums, temperature_minimums, choice=1, path="/matrixes/large"):
    files = [f for f in listdir(path) if isfile(join(get_script_path() + path, f))]

    print(files)
    for f in files:
        graph = Graph(f, choice)
        print("Wczytano graf " + graph.file_name + " z " + str(graph.number_of_cities) + " wierzchołkami")
        for tc in temperature_coefficients:
            for max in temperature_maximums:
                for min in temperature_minimums:
                    for a in range(repeats):
                        sa = SimulatedAnnealing(graph)

                        start = timer()
                        sa.start(max, min, tc)
                        end = timer()
                        time = format((end - start), '.8f')
                        print(str(min) + "\t" + str(max) + "\t" + str(tc) + "\t" + time + "\t" + str(
                            sa.best_cycle_cost) + "\n")
                        with open("./measurements/sa/" + f.rsplit(".", 1)[0] + ".txt", 'a+') as the_file:
                            the_file.write(str(min) + "\t" + str(max) + "\t" + str(tc) + "\t" + time + "\t" + str(
                                sa.best_cycle_cost) + "\n")
    print_to_continue()


def main():
    print("Testowanie algorytmu symulowanego wyżarzania\n")
    print("0. Małe macierze\n1. Duże macierze")
    choice = input("\nPodaj numer: ")
    if choice == "0":
        path = "./matrixes/small"
    elif choice == "1":
        path = "./matrixes/large"
    repeats = int(input("Podaj liczbę powtórzeń testów dla każdego z przypadków: "))
    temperature_coefficients = list(map(float, input("Podaj współczynniki wyżarzania odzielając je spacją: ").split(' ')))
    temperature_maximums = list(map(int, input("Podaj temepratury początkowe odzielając je spacją: ").split(' ')))
    temperature_minimums = list(map(float, input("Podaj temperatury końcowe odzielając je spacją: ").split(' ')))
    test(repeats, temperature_coefficients, temperature_maximums, temperature_minimums, int(choice), path)


if __name__ == "__main__":
    main()
