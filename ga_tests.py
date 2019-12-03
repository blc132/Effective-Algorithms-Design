from os import listdir
from os.path import isfile, join

from timeit import default_timer as timer
from graph import Graph
from main import print_to_continue
from genetic import Genetic

generations = {
    2000,
}

populations = [
    50,
]

cross_probs = [
    0.6,
]

mutat_probs = [
    0.15
]


def test(repeats):
    files = [f for f in listdir("./matrixes/small/") if isfile(join("./matrixes/small/", f))]

    print(files)
    for f in files:
        graph = Graph(f, 0)
        print("Wczytano graf z " + str(graph.number_of_cities) + " wierzchołkami")
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
                            with open("./measurements/" + f.rsplit(".", 1)[0] + ".txt", 'a+') as the_file:
                                the_file.write(text)
    print_to_continue()


def main():
    test(100)


if __name__ == "__main__":
    main()
