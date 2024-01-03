import pandas as pd
import io
import DijkstraSP as Alg


def find_shortest_paths_with_transits(network):
    transit_paths = {}
    for workstation in network.workstations:
        transit_paths[workstation['id']] = {}  # Use the node ID as the key
        for destination in range(network.node_count):
            if workstation['id'] != destination:
                optimal_path, transit_count = Alg.dijkstra_algorithm(network.network, workstation['id'], destination)
                transit_paths[workstation['id']][destination] = {"path": optimal_path,
                                                                 "transit_count": transit_count}
    return transit_paths


def transmit_message_virtual_channel(network, source, destination, message_size):
    # Логіка передачі повідомлення в режимі віртуального каналу

    # Отримати найкоротший маршрут від джерела до призначення
    shortest_path = network.transit_paths[source][destination]['path']

    # Симулювати передачу службових пакетів
    service_packets = len(shortest_path) - 2  # Виключити джерело та пункт призначення
    if service_packets == 0:
        info_packet_size = 0
    else:
        info_packet_size = int(message_size / service_packets)
    total_packet_size = info_packet_size + 1  # Інформаційний пакет + 1 для службового пакета

    # Сумарний час передачі
    transmission_time = sum(
        network.network[shortest_path[i]][shortest_path[i + 1]]['weight'] for i in range(len(shortest_path) - 1))

    return {
        "start_node": source,
        "end_node": destination,
        "service_packets": service_packets,
        "info_packets": service_packets,
        "info_packet_size": info_packet_size,
        "service_packet_size": 1,
        "total_packet_size": total_packet_size,
        "transmission_time": transmission_time
    }


def transmit_message_datagram(network, source, destination, message_size):
    # Логіка передачі повідомлення в режимі дейтаграми

    # Отримати найкоротший маршрут від джерела до призначення
    shortest_path = network.transit_paths[source][destination]['path']

    # Розрахувати сумарний час передачі на основі ваги каналу першої ребра
    transmission_time = sum(
        network.network[shortest_path[i]][shortest_path[i + 1]]['weight'] for i in range(len(shortest_path) - 1))

    return {
        "start_node": source,
        "end_node": destination,
        "service_packets": 0,
        "info_packets": 1,
        "info_packet_size": message_size,
        "service_packet_size": 0,
        "total_packet_size": message_size,
        "transmission_time": transmission_time
    }


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
        "Transfer Type": transfer_type,
        "Data Size (bytes)": data_size,
        "Unit Packet Size (bytes)": unit_packet_size,
        "Overhead Size (bytes)": overhead_traffic,
        "Transmission Duration (units)": time_to_transmit,
        "Total Information Packets": total_info_packets,
        "Actual Information Traffic (bytes)": actual_info_traffic,
        "Overhead Traffic (bytes)": overhead_traffic,
        "Duplex Mode": duplex_mode
    }


def execute_network_analysis(excel_filename="./project_data/network_performance_analysis.xlsx"):
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


def network_performance(network, source, destination, message_size):
    # Example for Virtual Channel mode
    transmission_result_vc = transmit_message_virtual_channel(network, source, destination, message_size)
    collect_statistics(transmission_result_vc)

    # Example for Datagram mode
    transmission_result_datagram = transmit_message_datagram(network, source, destination, message_size)
    collect_statistics(transmission_result_datagram)


def traffic_analysis(network):
    # розрахувати та зберегти таблицю результатів
    # запустити моделювання відправки повідомлення
    print("Analyzing network...")
    network.transit_paths = find_shortest_paths_with_transits(network)
    network.save_distance_table()

    start_point = int(input("Enter start point: "))

    for destination_workstation in network.workstations:
        destination = destination_workstation['id']
        if start_point != destination:
            network_performance(network, start_point, destination, 100)

    results = execute_network_analysis()
    print(results)


# Collect and print the statistics
def collect_statistics(transmission_result):
    print("Transmission Statistics:")
    print(f"Start Node: {transmission_result['start_node']}")
    print(f"End Node: {transmission_result['end_node']}")
    print(f"Service Packets: {transmission_result['service_packets']}")
    print(f"Information Packets: {transmission_result['info_packets']}")
    print(f"Information Packet Size: {transmission_result['info_packet_size']}")
    print(f"Service Packet Size: {transmission_result['service_packet_size']}")
    print(f"Total Packet Size: {transmission_result['total_packet_size']}")
    print(f"Transmission Time: {transmission_result['transmission_time']}")
    print("\n")
