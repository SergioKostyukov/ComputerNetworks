import NetworkModel
import TrafficAnalysis


def get_user_choice(data):
    # вибір типу каналів
    print("Enter channels type\n"
          "1. Full-Duplex\n"
          "2. Half-Duplex")
    choice = input("Enter your choice: ")
    if choice == 1:
        channelstype = "FULL-DUPLEX"
    else:
        channelstype = "HALF-DUPLEX"

    while True:
        print("\n"
              "1. Generate new random graph\n"
              "2. Load graph from file\n"
              "3. Show network\n"
              "4. Save graph to file\n"
              "5. Traffic analysis\n"
              "6. Exit")
        choice = input("Enter option number: ")

        if choice == '1':
            data.generate_network(channelstype)
        elif choice == '2':
            data.load_configuration("network_config.json")
        elif choice == '3':
            data.visualize_network()
        elif choice == '4':
            data.save_configuration("network_config.json")
        elif choice == '5':
            #start_vertex = int(input("Введіть початкову вершину: "))
            #end_vertex = int(input("Введіть кінцеву вершину: "))
            #paths = data.find_shortest_paths()

            data.transit_paths = data.find_shortest_paths_with_transits();
            data.display_distance_tables();

            # # Пошук найкоротшого шляху
            # shortest_path, path_length = dijkstra_shortest_path(user_graph, start_vertex, end_vertex)
            #
            # # Вивід шляху в консоль
            # print(f"Найкоротший шлях від вершини {start_vertex} до вершини {end_vertex}: {shortest_path}")
            # print(f"Час подолання шляху: {path_length:.2f} годин")
            #
            # # Візуалізація найкоротшого шляху червоним кольором
            # edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
            # nx.draw_networkx_edges(user_graph, pos_user_graph, edgelist=edges, edge_color='red', width=2)
        elif choice == '6':
            break
        else:
            print("Неправильний вибір. Спробуйте ще раз.")


def main():
    # Отримання графа з вибором користувача
    network = NetworkModel.DataTransmissionNetwork()
    get_user_choice(network)


if __name__ == "__main__":
    main()
