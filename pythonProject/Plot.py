import pandas as pd
import matplotlib.pyplot as plt


def show_graphics():
    while True:
        print("1. Message_size/Information_traffic\n"
              "2. Load graph from file\n"
              "3. Show network\n"
              "4. Save graph to file\n"
              "5. Exit")
        choice = input("Enter option number: ")

        if choice == '1':
            visualize_data()
        elif choice == '2':
            visualize_data()
        elif choice == '3':
            visualize_data()
        elif choice == '4':
            visualize_data()
        elif choice == '5':
            break
        else:
            print("Error input. Try again.")


def visualize_data(file_path="./project_data/traffic_analysis.xlsx"):
    df = pd.read_excel(file_path)

    # Розділення даних для VirtualLink та DatagramLink
    data_virtual = df[df['transmission_type'] == 'Virtual channel']
    data_datagram = df[df['transmission_type'] == 'Datagram']

    # Розмір даних та фактичний обсяг інформації для VirtualLink
    data_size_virtual = data_virtual['message_size']
    actual_traffic_virtual = data_virtual['information_traffic']
    # Розмір даних та фактичний обсяг інформації для DatagramLink
    data_size_datagram = data_datagram['message_size']
    actual_traffic_datagram = data_datagram['information_traffic']

    # Побудова графіку
    plt.figure(figsize=(10, 6))
    plt.plot(data_size_virtual, actual_traffic_virtual, marker='o', linestyle='-', color='red', label='VirtualLink')
    plt.plot(data_size_datagram, actual_traffic_datagram, marker='o', linestyle='--', color='blue',
             label='DatagramLink')

    plt.title('Залежність кількості службової інформації від розміру повідомлення')
    plt.xlabel('Розмір даних (байт)')
    plt.ylabel('Фактичний обсяг інформації (байт)')
    plt.grid(True)
    plt.legend()

    # Відображення графіку
    plt.show()
