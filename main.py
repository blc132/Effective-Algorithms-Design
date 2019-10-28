from bruteforce import BruteForce
from dynamicprogramming import DynamicProgramming
from graph import Graph
from os import system, name
import os


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def print_to_continue():
    input("Aby kontynuować wciśnij dowolny klawisz")


def main():
    graph = Graph()

    while 1:
        clear()
        print("Program do wyznaczania optymalnego cyklu Hamiltiona dla asymetrycznego problemu komiwojażera (ATSP)\n")

        if graph.number_of_cities != 0:
            print("Liczba wierzchołków aktualnie wczytanego grafu: " + str(graph.number_of_cities) + "\n")
        else:
            print("Aktualnie nie wczytano żadnego grafu\n")
        print("Wybierz funkcjonalność")
        print("1. Wczytaj małą macierz grafu")
        print("2. Wczytaj dużą macierz grafu")
        print("3. Wyświetl macierz kosztów")
        print("4. Wyświetl macierz sąsiedztwa")
        print("5. Rozwiąż problem komiwojażera za pomocą metody Brute Force")
        print("6. Rozwiąż problem komiwojażera za pomocą metody programowania dynamicznego")
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
            clear()
            if graph.number_of_cities != 0:
                graph.display_neighbourhood_matrix()
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '5':
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

        if choice == '6':
            if graph.file_name != "":
                dp = DynamicProgramming(graph)
                dp.start(0)
                print("Najlepszy cykl ma wagę: " + str(dp.best_cycle_cost))
                print("Optymalny cykl: ")
                dp.display_optimal_route()
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '7':
            print("Tests")
            print_to_continue()

        if choice == '8':
            print_to_continue()
            clear()
            return


if __name__ == '__main__':
    main()
