import pandas as pd
import DijkstraSP as Alg


# тип передачі
# розмір повідомлення
# розмір пакету
# розмір службової інформації
# час доставки повідомлень
# кількість інформаційних і службових пакетів
# інформаційний трафік
# управляючий трафік


# Temporary part
def execute_network_analysis(excel_filename="./project_data/traffic_analysis2.xlsx"):
    different_data_sizes = [500, 1500, 3000, 5000]

    performance_results = []
    for each_data_size in different_data_sizes:
        for transfer_mode in ['VirtualLink', 'DatagramLink']:
            for duplex_mode in ["FULL-DUPLEX", "HALF-DUPLEX"]:
                performance_results.append(evaluate_network_performance(
                    transfer_mode, each_data_size, duplex_mode))

    performance_data_table = pd.DataFrame(performance_results)

    performance_data_table.to_excel(excel_filename, index=False)


def evaluate_network_performance(transmission_type, message_size, duplex_mode):
    packet_size = 1000
    overhead_size = 100
    link_speed = 1000000

    info_packets_count = message_size // packet_size
    if message_size % packet_size > 0:
        info_packets_count += 1

    if transmission_type == 'VirtualLink':
        overhead_traffic = overhead_size
    elif transmission_type == 'DatagramLink':
        overhead_traffic = overhead_size * info_packets_count

    information_traffic = info_packets_count * packet_size
    complete_traffic = information_traffic + overhead_traffic

    if duplex_mode == "FULL-DUPLEX":
        delivery_time = complete_traffic * 8 / link_speed
    elif duplex_mode == "HALF-DUPLEX":
        delivery_time = complete_traffic * 8 / (link_speed / 2)

    return {
        "transmission_type": transmission_type,  # +
        "message_size": message_size,  # +
        "packet_size": packet_size,  # +
        "overhead_size": overhead_traffic,  # +
        "delivery_time": delivery_time,  # +
        "info_packets_count": info_packets_count,
        "information_traffic": information_traffic,  # +
        "control_traffic": overhead_traffic,
        "duplex_mode": duplex_mode  # +
    }


# Main part
def transmit_message_virtual_channel(duplex_mode, network, source, destination, message_size, packet_size):
    link_speed = 1000000
    path = network.transit_paths[source][destination]['path']

    total_weight = network.transit_paths[source][destination]['transit_count']

    info_packets_count = message_size // packet_size
    if message_size % packet_size > 0:
        info_packets_count += 1

    # Параметри передачі
    total_channels_count = len(path)
    transmission_type = "Virtual channel"
    overhead_size = (total_channels_count + info_packets_count - 1) * 32

    # Метрики трафіку
    information_traffic = message_size * info_packets_count * 32
    control_traffic = overhead_size * total_weight

    # Час доставки
    if duplex_mode == "FULL-DUPLEX":
        delivery_time = (information_traffic + control_traffic) * 8 / link_speed
    elif duplex_mode == "HALF-DUPLEX":
        delivery_time = (information_traffic + control_traffic) * 8 / (link_speed / 2)

    return {
        "transmission_type": transmission_type,  # +
        "message_size": message_size,  # +
        "packet_size": packet_size,  # +
        "overhead_size": overhead_size,
        "delivery_time": delivery_time,
        "info_packets_count": info_packets_count,
        "information_traffic": information_traffic,  # +
        "control_traffic": control_traffic,
        "duplex_mode": duplex_mode  # +
    }


def transmit_message_datagram(duplex_mode, network, source, destination, message_size, packet_size):
    link_speed = 1000000
    path = network.transit_paths[source][destination]['path']
    info_packets_count = message_size // packet_size
    if message_size % packet_size > 0:
        info_packets_count += 1

    # Параметри передачі
    transmission_type = "Datagram"
    overhead_size = info_packets_count * 32

    # Метрики трафіку
    information_traffic = info_packets_count * message_size * 32
    control_traffic = overhead_size * len(path)

    # Час доставки
    if duplex_mode == "FULL-DUPLEX":
        delivery_time = (information_traffic + control_traffic) * 8 / link_speed
    elif duplex_mode == "HALF-DUPLEX":
        delivery_time = (information_traffic + control_traffic) * 8 / (link_speed / 2)

    return {
        "transmission_type": transmission_type,  # +
        "message_size": message_size,  # +
        "packet_size": packet_size,  # +
        "overhead_size": overhead_size,
        "delivery_time": delivery_time,
        "info_packets_count": info_packets_count,
        "information_traffic": information_traffic,  # +
        "control_traffic": control_traffic,
        "duplex_mode": duplex_mode  # +
    }


def network_performance(network, source, destination, filename="./project_data/traffic_analysis.xlsx"):
    different_data_sizes = [500, 1000, 2000, 3000, 4000, 5000, 7000, 10000]
    packet_size = 1000
    duplex_modes = ["FULL-DUPLEX", "HALF-DUPLEX"]

    performance_results = []
    for duplex_mode in duplex_modes:
        for each_data_size in different_data_sizes:
            performance_results.append(
                transmit_message_virtual_channel(duplex_mode, network, source, destination, each_data_size,
                                                 packet_size))
            performance_results.append(
                transmit_message_datagram(duplex_mode, network, source, destination, each_data_size, packet_size))

    performance_data_table = pd.DataFrame(performance_results)

    performance_data_table.to_excel(filename, index=False)


def traffic_analysis(network):
    print("Analyzing network...")

    network.transit_paths = find_shortest_paths_with_transits(network)
    network.save_distance_table()

    start_point = int(input("Enter start point: "))
    end_point = int(input("Enter end point: "))

    network_performance(network, start_point, end_point)

    execute_network_analysis()


def find_shortest_paths_with_transits(network):
    transit_paths = {}
    for workstation in network.workstations:
        transit_paths[workstation['id']] = {}
        for destination in range(network.node_count):
            if workstation['id'] != destination:
                optimal_path, transit_count = Alg.dijkstra_algorithm(network.network, workstation['id'], destination)
                transit_paths[workstation['id']][destination] = {"path": optimal_path,
                                                                 "transit_count": transit_count}
    return transit_paths
