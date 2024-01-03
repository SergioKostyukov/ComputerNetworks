import pandas as pd
import io
import DijkstraSP as dsp


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


def execute_network_analysis(data, excel_filename="./project_data/network_performance_analysis.xlsx"):
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


def traffic_analysis(network):
    # знайти та зберегти таблицю коротших шляхів
    # побудувати таблицю результаті
    print("Analyzing network...")
    network.transit_paths = network.find_shortest_paths_with_transits()
    network.display_distance_tables()

    start_vertex = int(input("Enter start point: "))
    end_vertex = int(input("Enter end point: "))

    # Example for Virtual Channel mode
    transmission_result_vc = network.transmit_message_virtual_channel(start_vertex, end_vertex, 100)
    network.collect_statistics(transmission_result_vc)

    # Example for Datagram mode
    transmission_result_datagram = network.transmit_message_datagram(start_vertex, end_vertex, 100)
    network.collect_statistics(transmission_result_datagram)

    results = execute_network_analysis(network)
    print(results)

    # Пошук найкоротшого шляху
    # shortest_path, path_length = dsp.dijkstra_algorithm(data.network, start_vertex, end_vertex)
    #
    # Вивід шляху в консоль
    # print(f"Найкоротший шлях від вершини {start_vertex} до вершини {end_vertex}: {shortest_path}")
    # print(f"Час подолання шляху: {path_length:.2f} годин")
    #
    # # Візуалізація найкоротшого шляху червоним кольором
    # edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
    # nx.draw_networkx_edges(user_graph, pos_user_graph, edgelist=edges, edge_color='red', width=2)
