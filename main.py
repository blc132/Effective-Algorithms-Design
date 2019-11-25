from timeit import default_timer as timer

from algorithms.bruteforce import BruteForce
from algorithms.dynamicprogramming import DynamicProgramming
from graph.graph import Graph
from os import system, name
import os

from algorithms.simulatedannealing import SimulatedAnnealing


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def print_to_continue():
    input("Aby kontynuować wciśnij dowolny klawisz")


def test(graph):

    clear()
    repeats = int(input("Liczba powtórzeń: "))

    while 1:
        clear()
        print("Możliwości do wyboru:\n")
        print("1. Brute Force")
        print("2. Programowanie dynamiczne")
        print("3. Symulowane wyżarzanie")
        print("4. Powrót do głównego menu")
        choice = input("\nPodaj numer: ")
        if choice == '1':
            start = timer()
            for x in range(repeats):
                bf = BruteForce(graph)
                bf.start(0)

            end = timer()
            time = format((end - start) / repeats, '.8f')
            print(time)
            with open('bf_measurement.txt', 'a+') as the_file:
                the_file.write(graph.file_name + "\n" + time + "\n")
            print_to_continue()

        if choice == '2':
            start = timer()
            for x in range(repeats):
                dp = DynamicProgramming(graph)
                dp.start(0)

            end = timer()
            time = format((end - start) / repeats, '.8f')
            print(time)
            with open('dp_measurement.txt', 'a+') as the_file:
                the_file.write(graph.file_name + "\n" + time + "\n")
            print_to_continue()

        if choice == '3':
            start = timer()
            for x in range(repeats):
                dp = DynamicProgramming(graph)
                dp.start(0)

            end = timer()
            time = format((end - start) / repeats, '.8f')
            print(time)
            with open('dp_measurement.txt', 'a+') as the_file:
                the_file.write(graph.file_name + "\n" + time + "\n")
            print_to_continue()

        if choice == '4':
            return


def main():
    graph = Graph()

    while 1:
        clear()
        print("Program do wyznaczania optymalnego cyklu Hamiltiona dla problemu komiwojażera\n")

        if graph.number_of_cities != 0:
            print("Liczba wierzchołków aktualnie wczytanego grafu: " + str(graph.number_of_cities) + "\n")
        else:
            print("Aktualnie nie wczytano żadnego grafu\n")
        print("Wybierz funkcjonalność")
        print("1. Wczytaj małą macierz grafu")
        print("2. Wczytaj dużą macierz grafu")
        print("3. Wyświetl macierz kosztów")
        print("4. Rozwiąż problem komiwojażera za pomocą metody Brute Force")
        print("5. Rozwiąż problem komiwojażera za pomocą metody programowania dynamicznego")
        print("6. Rozwiąż problem komiwojażera za pomocą metody symulowanego wyżarzania")
        print("7. Przeprowadź testy seryjne")
        print("8. Zakończ działanie programu")
        choice = input("\nPodaj numer: ")
        if choice == '1':
            clear()
            print("Lista dostępnych plików:\n-----------")
            print(*os.listdir("./matrixes/small/"), sep='\n')
            print("-----------")
            file_name = input("Podaj nazwę pliku z małym grafem: ")
            graph = Graph(file_name, 0)
            print("Wczytano graf z " + str(graph.number_of_cities) + " wierzchołkami\nAby kontynuwać wciśnij dowolny "
                                                                     "klawisz")
            choice = 0
            input()

        if choice == '2':
            clear()
            print("Podaj nazwę pliku z dużym grafem")
            print(*os.listdir("./matrixes/large/"), sep='\n')
            file_name = input()
            graph = Graph(file_name, 1)
            print("Wczytano graf z " + str(graph.number_of_cities) + " wierzchołkami")
            print_to_continue()
            choice = 0

        if choice == '3':
            clear()
            if graph.number_of_cities != 0:
                graph.display_cost_matrix()
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '4':
            if graph.file_name != "":
                bf = BruteForce(graph)
                bf.starting_vertex = 0
                bf.start(0)
                print("Najlepszy cykl ma wagę: " + str(bf.best_cycle_cost))
                print("Optymalny cykl: ")
                bf.display_optimal_route()
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '5':
            if graph.file_name != "":
                dp = DynamicProgramming(graph)
                dp.start(0)
                print("Najlepszy cykl ma wagę: " + str(dp.best_cycle_cost))
                print("Optymalny cykl: ")
                dp.display_optimal_route()
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '6':
            # graph = Graph("tsp_10.txt", 0)
            if graph.file_name != "":
                # t_0 = float(input("Temperatura początkowa wyżarzania: "))
                # t_min = float(input("Temperatura minimalna wyżarzania: "))
                # t_coefficient = float(input("Współczynnik wyżarzania z zakresu (0,1): "))

                sa = SimulatedAnnealing(graph)
                # sa.start(t_0, t_min, t_coefficient)
                start = timer()
                sa.start(1000, 1, 0.999)
                end = timer()
                time = format(end - start, '.8f')
                print(time)
                print("Najlepszy cykl ma wagę: " + str(sa.best_cycle_cost))
                print("Optymalny cykl: ")
                sa.display_optimal_route()
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '7':
            if graph.file_name != "":
                test(graph)
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '8':
            print_to_continue()
            clear()
            return


if __name__ == '__main__':
    main()
