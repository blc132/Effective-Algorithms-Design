from os import listdir
from os.path import isfile, join

from timeit import default_timer as timer
from graph import Graph
from main import print_to_continue
from simulatedannealing import SimulatedAnnealing

temperature_coefficients = {
    0.9,
    0.99,
}

temperature_maximums = [
    1000,
]

temperature_minimums = [
    0.0001
]


def test(repeats):
    files = [f for f in listdir("./matrixes/sa_graphs/") if isfile(join("./matrixes/sa_graphs/", f))]

    print(files)
    for f in files:
        graph = Graph(f, 3)
        print("Wczytano graf z " + str(graph.number_of_cities) + " wierzchołkami")
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
                        with open("./measurements/" + f.rsplit(".", 1)[0] + ".txt", 'a+') as the_file:
                            the_file.write(str(min) + "\t" + str(max) + "\t" + str(tc) + "\t" + time + "\t" + str(
                                sa.best_cycle_cost) + "\n")
    print_to_continue()


def main():
    print("Hello World!")
    test(10)


if __name__ == "__main__":
    main()
