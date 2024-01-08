import pandas as pd
import DijkstraSP as Alg


def transmit_message_virtual_channel(duplex_mode, network, source, destination, message_size, packet_size):
    path = network.transit_paths[source][destination]['path']
    total_weight = network.transit_paths[source][destination]['transit_count']

    info_packets_count = message_size // (packet_size - 20)
    if message_size % packet_size > 0:
        info_packets_count += 1

    # Параметри передачі
    transmission_type = "Virtual channel"
    overhead_size = (3 + info_packets_count * 2) * 20

    # Метрики трафіку
    information_traffic = message_size * info_packets_count * 32
    control_traffic = overhead_size * total_weight

    # Час доставки
    delivery_time = (message_size + overhead_size)
    if duplex_mode == "HALF-DUPLEX":
        delivery_time /= 2

    return {
        "transmission_type": transmission_type,  # +
        "message_size": message_size,  # +
        "packet_size": packet_size,  # +
        "overhead_size": overhead_size,  # +
        "delivery_time": delivery_time,  # +
        "info_packets": info_packets_count * 32,
        "information_traffic": information_traffic,  # +
        "control_traffic": control_traffic,
        "duplex_mode": duplex_mode  # +
    }


def transmit_message_datagram(duplex_mode, network, source, destination, message_size, packet_size):
    path = network.transit_paths[source][destination]['path']
    total_weight = network.transit_paths[source][destination]['transit_count']

    info_packets_count = message_size // (packet_size - 8)
    if message_size % packet_size > 0:
        info_packets_count += 1

    # Параметри передачі
    transmission_type = "Datagram"
    overhead_size = info_packets_count * 8 # * 4

    # Метрики трафіку
    information_traffic = info_packets_count * message_size * 32
    control_traffic = overhead_size * total_weight

    # Час доставки
    delivery_time = (message_size + overhead_size) / 2
    if duplex_mode == "HALF-DUPLEX":
        delivery_time /= 2

    return {
        "transmission_type": transmission_type,  # тип передачі +
        "message_size": message_size,  # розмір повідомлення +
        "packet_size": packet_size,  # розмір пакету +
        "overhead_size": overhead_size,  # розмір службової інформації
        "delivery_time": delivery_time,  # час доставки повідомлень
        "info_packets": info_packets_count * 32,  # кількість інформаційних
        "information_traffic": information_traffic,  # інформаційний трафік +
        "control_traffic": control_traffic,  # управляючий трафік
        "duplex_mode": duplex_mode  # +
    }


def network_performance(network, source, destination, filename="./project_data/traffic_analysis_data.xlsx"):
    different_data_sizes = [500, 1000, 2000, 3000, 4000, 5000, 7000, 10000]
    different_packet_sizes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    packet_size = 1000
    data_size = 10000
    duplex_modes = ["FULL-DUPLEX", "HALF-DUPLEX"]

    # Calculate for different data size
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

    # Calculate for different packet size
    performance_results.clear()
    for duplex_mode in duplex_modes:
        for each_packet_size in different_packet_sizes:
            performance_results.append(
                transmit_message_virtual_channel(duplex_mode, network, source, destination, data_size,
                                                 each_packet_size))
            performance_results.append(
                transmit_message_datagram(duplex_mode, network, source, destination, data_size, each_packet_size))

    performance_data_table = pd.DataFrame(performance_results)

    filename = "./project_data/traffic_analysis_packet.xlsx"
    performance_data_table.to_excel(filename, index=False)


def traffic_analysis(network):
    print("Analyzing network...")

    network.transit_paths = find_shortest_paths_with_transits(network)
    network.save_distance_table()

    start_point = int(input("Enter start point: "))
    end_point = int(input("Enter end point: "))

    path = network.transit_paths[start_point][end_point]['path']
    print(path)

    network_performance(network, start_point, end_point)


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
