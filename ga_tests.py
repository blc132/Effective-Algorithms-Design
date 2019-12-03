from os import listdir, path
from os.path import isfile, join
import sys
from timeit import default_timer as timer
from graph import Graph
from main import print_to_continue
from genetic import Genetic


def get_script_path():
    return path.dirname(path.realpath(sys.argv[0]))

# generations = {
#     2000,
# }
#
# populations = [
#     50,
# ]
#
# cross_probs = [
#     0.6,
# ]
#
# mutat_probs = [
#     0.15
# ]

# path = "./matrixes/large"


def test(repeats, generations, populations, cross_probs, mutat_probs, choice=1, path="/matrixes/large"):
    files = [f for f in listdir(path) if isfile(join(get_script_path() + path, f))]

    print(files)
    for f in files:
        graph = Graph(f, choice)
        print("Wczytano graf " + graph.file_name + " z " + str(graph.number_of_cities) + " wierzchołkami")
        for generation in generations:
            for population in populations:
                for cross_prob in cross_probs:
                    for mutat_prob in mutat_probs:
                        for a in range(repeats):
                            ga = Genetic(graph)

                            start = timer()
                            ga.start(generation, population, cross_prob, mutat_prob)
                            end = timer()
                            time = format((end - start), '.8f')
                            text = (str(generation) + "\t" + str(population) + "\t" + str(cross_prob) + "\t" + str(
                                mutat_prob) + "\t" + time + "\t" + str(ga.best_cycle_cost) + "\n").replace('.', ',')
                            print(text)
                            with open("./measurements/ga/" + f.rsplit(".", 1)[0] + ".txt", 'a+') as the_file:
                                the_file.write(text)
    print_to_continue()


def main():
    print("Testowanie algorytmu genetycznego\n")
    print("0. Małe macierze\n1. Duże macierze")
    choice = input("\nPodaj numer: ")
    if choice == "0":
        path = "/matrixes/small"
    elif choice == "1":
        path = "/matrixes/large"
    repeats = int(input("Podaj liczbę powtórzeń testów dla każdego z przypadków: "))
    generations = list(map(int, input("Podaj generacje odzielając je spacją: ").split(' ')))
    populations = list(map(int, input("Podaj populacje odzielając je spacją: ").split(' ')))
    cross_probs = list(map(float, input("Podaj prawdopodobieństwa krzyżowania odzielając je spacją: ").split(' ')))
    mutat_probs = list(map(float, input("Podaj prawdopodobieństwa mutacji odzielając je spacją: ").split(' ')))
    test(repeats, generations, populations, cross_probs, mutat_probs, int(choice), path)


if __name__ == "__main__":
    main()
