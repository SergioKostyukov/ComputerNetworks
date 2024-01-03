import NetworkModel
import TrafficAnalysis as Analysis
import Plot


# 1 система моделювання відправки повідомлення
#
# 1 побудова графіків для аналізу
#
# 2 проблема з завантаженням з файлу
#
# 3 коментарі
# 3 чистий код

def get_user_choice(network):
    while True:
        print("1. Generate new random graph\n"
              "2. Load graph from file\n"
              "3. Show network\n"
              "4. Save graph to file\n"
              "5. Traffic analysis\n"
              "6. Show graphics\n"
              "7. Exit")
        choice = input("Enter option number: ")

        if choice == '1':
            print("\nEnter channels type\n"
                  "1. FULL-DUPLEX\n"
                  "2. HALF-DUPLEX")
            choice = input("Enter your choice: ")
            if choice == 1:
                channelstype = "FULL-DUPLEX"
            else:
                channelstype = "HALF-DUPLEX"

            network.generate_network(channelstype)
        elif choice == '2':
            network.load_configuration()
        elif choice == '3':
            network.visualize_network()
        elif choice == '4':
            network.save_configuration()
        elif choice == '5':
            Analysis.traffic_analysis(network)
        elif choice == '6':
            Plot.show_graphics()
        elif choice == '7':
            break
        else:
            print("Error input. Try again.")


def main():
    network = NetworkModel.DataTransmissionNetwork()
    get_user_choice(network)


if __name__ == "__main__":
    main()
