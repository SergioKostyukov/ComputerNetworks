import pandas as pd
import matplotlib.pyplot as plt


def show_graphics():
    while True:
        print("1. Overhead_size/Message_size FULL-DUPLEX\n"
              "2. Delivery_time/Message_size FULL-DUPLEX\n"
              "3. Overhead_size/Packet_size FULL-DUPLEX\n"
              "4. Delivery_time/Packet_size FULL-DUPLEX\n\n"
              "5. Overhead_size/Message_size HALF-DUPLEX\n"
              "6. Delivery_time/Message_size HALF-DUPLEX\n"
              "7. Overhead_size/Packet_size HALF-DUPLEX\n"
              "8. Delivery_time/Packet_size HALF-DUPLEX\n"
              "9. Exit")
        choice = input("Enter option number: ")

        if choice == '1':
            visualize_data("Message", "Overhead", "FULL")
        elif choice == '2':
            visualize_data('Message', 'Delivery', "FULL")
        elif choice == '3':
            visualize_data('Packet', 'Overhead', "FULL")
        elif choice == '4':
            visualize_data('Packet', 'Delivery', "FULL")
        elif choice == '5':
            visualize_data('Message', 'Overhead', "HALF")
        elif choice == '6':
            visualize_data('Message', 'Delivery', "HALF")
        elif choice == '7':
            visualize_data('Packet', 'Overhead', "HALF")
        elif choice == '8':
            visualize_data('Packet', 'Delivery', "HALF")
        elif choice == '9':
            break
        else:
            print("Error input. Try again.")


def visualize_data(table_type, param, duplex, file_path="./project_data/traffic_analysis_data.xlsx"):
    if table_type == 'Packet':
        file_path = "./project_data/traffic_analysis_packet.xlsx"

    try:
        df = pd.read_excel(file_path)

        # Розділення даних для VirtualLink та DatagramLink з поділом за duplex_mode
        if duplex == 'FULL':
            data_virtual = df[
                (df['transmission_type'] == 'Virtual channel') & (df['duplex_mode'] == 'FULL-DUPLEX')]
            data_datagram = df[(df['transmission_type'] == 'Datagram') & (df['duplex_mode'] == 'FULL-DUPLEX')]
        else:
            data_virtual = df[
                (df['transmission_type'] == 'Virtual channel') & (df['duplex_mode'] == 'HALF-DUPLEX')]
            data_datagram = df[(df['transmission_type'] == 'Datagram') & (df['duplex_mode'] == 'HALF-DUPLEX')]

        if table_type == 'Packet' and param == 'Overhead':
            # Для VirtualLink
            param_virtual = data_virtual['overhead_size']
            size_virtual = data_virtual['packet_size']
            # Для DatagramLink
            param_datagram = data_datagram['overhead_size']
            size_datagram = data_datagram['packet_size']

            plt.title('Overhead Size / Packet Size')
            plt.xlabel('packet_size')
            plt.ylabel('overhead_size')
        elif table_type == 'Packet' and param == 'Delivery':
            # Для VirtualLink
            param_virtual = data_virtual['delivery_time']
            size_virtual = data_virtual['packet_size']
            # Для DatagramLink
            param_datagram = data_datagram['delivery_time']
            size_datagram = data_datagram['packet_size']

            plt.title('Delivery Time / Packet Size')
            plt.xlabel('packet_size')
            plt.ylabel('delivery_time')
        elif table_type == "Message" and param == "Overhead":
            # Для VirtualLink
            param_virtual = data_virtual['overhead_size']
            size_virtual = data_virtual['message_size']
            # Для DatagramLink
            param_datagram = data_datagram['overhead_size']
            size_datagram = data_datagram['message_size']

            plt.title('Overhead Size / Message Size')
            plt.xlabel('message_size')
            plt.ylabel('overhead_size')
        elif table_type == 'Message' and param == 'Delivery':
            # Для VirtualLink
            param_virtual = data_virtual['delivery_time']
            size_virtual = data_virtual['message_size']
            # Для DatagramLink
            param_datagram = data_datagram['delivery_time']
            size_datagram = data_datagram['message_size']

            plt.title('Delivery Time / Message Size')
            plt.xlabel('message_size')
            plt.ylabel('delivery_time')
        else:
            print("Error\n")

        # Побудова графіку
        plt.figure(figsize=(10, 6))
        plt.plot(size_virtual, param_virtual, marker='o', linestyle='-', color='red', label='VirtualLink')
        plt.plot(size_datagram, param_datagram, marker='o', linestyle='--', color='blue',
                 label='DatagramLink')

        if table_type == 'Packet' and param == 'Overhead':
            plt.title('Overhead Size / Packet Size')
            plt.xlabel('packet_size')
            plt.ylabel('overhead_size')
        elif table_type == 'Packet' and param == 'Delivery':
            plt.title('Delivery Time / Packet Size')
            plt.xlabel('packet_size')
            plt.ylabel('delivery_time')
        elif table_type == "Message" and param == "Overhead":
            plt.title('Overhead Size / Message Size')
            plt.xlabel('message_size')
            plt.ylabel('overhead_size')
        else:
            plt.title('Delivery Time / Message Size')
            plt.xlabel('message_size')
            plt.ylabel('delivery_time')

        plt.grid(True)
        plt.legend()

        # Відображення графіку
        plt.show()
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        print("The file is empty. Please check the file content.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
