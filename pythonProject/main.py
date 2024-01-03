import NetworkModel
import TrafficAnalysis as ta


# 1 зміна алгоритму пошуку коротших шляхів
# 1 вплив типу каналів на результат
# 1 корегування результатів підрахунків відповідно до завдання
#
# 2 занесення результатів вимірів у файли
# 2 індексація робочих станцій при знаходженні найкоротшого шляху
#
# 3 відображення коротшого шляху графічно
# 3 побудова графіків для аналізу
#
# 4 проблема з завантаженням з файлу
#
# 5 коментарі
# 5 чистий код

def get_user_choice(network):
    print("Enter channels type\n"
          "1. FULL-DUPLEX\n"
          "2. HALF-DUPLEX")
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
            network.generate_network(channelstype)
        elif choice == '2':
            network.load_configuration()
        elif choice == '3':
            network.visualize_network()
        elif choice == '4':
            network.save_configuration()
        elif choice == '5':
            ta.traffic_analysis(network)
        elif choice == '6':
            break
        else:
            print("Error input. Try again.")


def main():
    network = NetworkModel.DataTransmissionNetwork()
    get_user_choice(network)


if __name__ == "__main__":
    main()
