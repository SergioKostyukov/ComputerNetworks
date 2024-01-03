import pandas as pd
import io
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
def evaluate_network_performance(transfer_type, data_size, unit_packet_size, overhead_size, link_speed, duplex_mode):
    total_info_packets = data_size // unit_packet_size
    if data_size % unit_packet_size > 0:
        total_info_packets += 1

    if transfer_type == 'VirtualLink':
        overhead_traffic = overhead_size
    elif transfer_type == 'DatagramLink':
        overhead_traffic = overhead_size * total_info_packets

    actual_info_traffic = total_info_packets * unit_packet_size
    complete_traffic = actual_info_traffic + overhead_traffic

    if duplex_mode == "FULL-DUPLEX":
        time_to_transmit = complete_traffic * 8 / link_speed
    elif duplex_mode == "HALF-DUPLEX":
        time_to_transmit = complete_traffic * 8 / (link_speed / 2)

    return {
        "transmission_type": transfer_type,
        "message_size": data_size,
        "total_packet_size": unit_packet_size,
        "overhead_size": overhead_traffic,
        "delivery_time": time_to_transmit,
        "info_packets_count": total_info_packets,
        "information_traffic": actual_info_traffic,
        "control_traffic": overhead_traffic,
        "Duplex Mode": duplex_mode
    }


def execute_network_analysis(excel_filename="./project_data/traffic_analysis2.xlsx"):
    basic_packet_size = 1000
    overhead_packet_size = 100
    network_bandwidth = 1000000
    different_data_sizes = [500, 1500, 3000, 5000]
    duplex_modes = ["FULL-DUPLEX", "HALF-DUPLEX"]

    performance_results = []
    for each_data_size in different_data_sizes:
        for transfer_mode in ['VirtualLink', 'DatagramLink']:
            for duplex_mode in duplex_modes:
                performance_results.append(evaluate_network_performance(
                    transfer_mode, each_data_size, basic_packet_size,
                    overhead_packet_size, network_bandwidth, duplex_mode))

    performance_data_table = pd.DataFrame(performance_results)

    performance_data_table.to_excel(excel_filename, index=False)

    output = io.StringIO()
    performance_data_table.to_string(output)
    table_string = output.getvalue()
    output.close()

    return table_string


# Main part
def transmit_message_virtual_channel(network, source, destination, message_size):
    path = network.transit_paths[source][destination]['path']
    total_weight = sum(network.network[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))

    # Параметри передачі
    transmission_type = "Virtual channel"
    information_packet_size = message_size
    overhead_size = 0  # Нуль для віртуального каналу
    total_packet_size = information_packet_size + overhead_size

    # Метрики трафіку
    information_traffic = information_packet_size * total_weight
    control_traffic = overhead_size * total_weight

    # Час доставки
    delivery_time = total_weight  # За припущенням, що час передачі на одиницю ваги

    # Кількість інформаційних і службових пакетів
    info_packets_count = 1
    control_packets_count = 0  # Нуль для віртуального каналу

    return {
        "transmission_type": transmission_type,
        "message_size": message_size,
        "total_packet_size": total_packet_size,
        "overhead_size": overhead_size,
        "delivery_time": delivery_time,
        "info_packets_count": info_packets_count,
        "control_packets_count": control_packets_count,
        "information_traffic": information_traffic,
        "control_traffic": control_traffic
    }


def transmit_message_datagram(network, source, destination, message_size):
    path = network.transit_paths[source][destination]['path']

    # Параметри передачі
    transmission_type = "Datagram"
    information_packet_size = message_size
    overhead_size = 0  # Нуль для дейтаграмного режиму
    total_packet_size = information_packet_size + overhead_size

    # Метрики трафіку
    information_traffic = information_packet_size * len(path)
    control_traffic = overhead_size * len(path)

    # Час доставки
    delivery_time = len(path)  # За припущенням, що час передачі на один вузол мережі

    # Кількість інформаційних і службових пакетів
    info_packets_count = len(path)
    control_packets_count = 0  # Нуль для дейтаграмного режиму

    return {
        "transmission_type": transmission_type,
        "message_size": message_size,
        "total_packet_size": total_packet_size,
        "overhead_size": overhead_size,
        "delivery_time": delivery_time,
        "info_packets_count": info_packets_count,
        "control_packets_count": control_packets_count,
        "information_traffic": information_traffic,
        "control_traffic": control_traffic
    }


def network_performance(network, source, destination, filename="./project_data/traffic_analysis.xlsx"):
    different_data_sizes = [500, 1500, 3000, 5000]
    duplex_modes = ["FULL-DUPLEX", "HALF-DUPLEX"]

    performance_results = []
    for each_data_size in different_data_sizes:
        performance_results.append(transmit_message_virtual_channel(network, source, destination, each_data_size))
        performance_results.append(transmit_message_datagram(network, source, destination, each_data_size))

    performance_data_table = pd.DataFrame(performance_results)

    performance_data_table.to_excel(filename, index=False)

    output = io.StringIO()
    performance_data_table.to_string(output)
    table_string = output.getvalue()
    output.close()

    return table_string


def traffic_analysis(network):
    print("Analyzing network...")
    network.transit_paths = find_shortest_paths_with_transits(network)
    network.save_distance_table()

    start_point = int(input("Enter start point: "))
    end_point = int(input("Enter end point: "))
    results = network_performance(network, start_point, end_point)
    print(results)

    results = execute_network_analysis()
    print(results)


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
