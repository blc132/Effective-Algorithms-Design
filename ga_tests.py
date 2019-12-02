from os import listdir
from os.path import isfile, join

from timeit import default_timer as timer
from graph import Graph
from main import print_to_continue
from genetic import Genetic

# (size_of_population, number_of_generations, cross_probability, mutation_probability)
generations = {
    100,
    500,
    1000,
}

populations = [
    100,
    500,
    1000,
]

cross_probs = [
    0.3,
    0.6,
    0.8,
]

mutat_probs = [
    0.05,
    0.10,
    0.15
]


def test(repeats):
    files = [f for f in listdir("./matrixes/ga_graphs/") if isfile(join("./matrixes/ga_graphs/", f))]

    print(files)
    for f in files:
        graph = Graph(f, 3)
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
    print("Hello World!")
    test(5)


if __name__ == "__main__":
    main()
