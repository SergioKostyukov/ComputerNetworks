import networkx as nx
import matplotlib.pyplot as plt
import random
import json
import itertools
import pandas as pd


class DataTransmissionNetwork:
    def __init__(self):
        self.network = nx.Graph()
        self.type = "FULL-DUPLEX"
        self.node_count = 24
        self.degree = 4
        self.channels = [1, 2, 4, 5, 6, 7, 8, 10, 15, 21]
        self.workstationid = [2, 4, 8, 12, 17, 22]
        self.workstations = [i for i in range(3, self.node_count, self.degree)]
        self.transit_paths = {}

    def generate_network(self, chtype):
        while True:
            m = int(self.node_count * self.degree / 2)
            self.network = nx.gnm_random_graph(self.node_count, m)

            # Check if the graph is connected
            if nx.is_connected(self.network):
                break

        # генерація ваг та типу для зв'язків
        for edge in self.network.edges():
            self.network[edge[0]][edge[1]]['weight'] = random.choice(self.channels)
            self.network[edge[0]][edge[1]]['type'] = chtype

        # генерація робочих станцій для вузлів з self.workstationid
        self.workstations = []  # Clear the list before populating
        count = 1
        for i in self.workstationid:
            workstation_node = self.node_count + count
            count += 1
            self.network.add_node(workstation_node)
            weight = random.choice(self.channels)
            self.network.add_edge(workstation_node, i, weight=weight, type=chtype)
            self.workstations.append({"node": i, "channel_type": chtype, "channel_weight": weight})

        # Additional logic to add two edges with type "SIMPLEX"
        simplex_edges = list(itertools.combinations(range(self.node_count), 2))[:2]
        for edge in simplex_edges:
            self.network.add_edge(edge[0], edge[1], weight=random.choice(self.channels), type="SIMPLEX")

    def save_configuration(self, filename="./project_data/network_config.json"):
        data = {
            "network": nx.to_dict_of_dicts(self.network),
            "workstations": self.workstations
        }
        with open(filename, "w") as file:
            json.dump(data, file)

    def load_configuration(self, filename="./project_data/network_config.json"):
        with open(filename, "r") as file:
            data = json.load(file)
            self.network = nx.DiGraph(data["network"])
            self.workstations = data["workstations"]

    def find_shortest_paths_with_transits(self):
        transit_paths = {}
        for workstation in self.workstations:
            transit_paths[workstation['node']] = {}  # Use the node ID as the key
            for destination in range(self.node_count):
                if workstation['node'] != destination:
                    shortest_path = nx.shortest_path(self.network, source=workstation['node'], target=destination,
                                                     weight="weight")
                    transit_count = len(shortest_path) - 2  # Number of transit nodes
                    transit_paths[workstation['node']][destination] = {"path": shortest_path,
                                                                       "transit_count": transit_count}
        return transit_paths

    def transmit_message_virtual_channel(self, source, destination, message_size):
        # Логіка передачі повідомлення в режимі віртуального каналу

        # Отримати найкоротший маршрут від джерела до призначення
        shortest_path = self.transit_paths[source][destination]['path']

        # Симулювати передачу службових пакетів
        service_packets = len(shortest_path) - 2  # Виключити джерело та пункт призначення
        info_packet_size = int(message_size / service_packets)
        total_packet_size = info_packet_size + 1  # Інформаційний пакет + 1 для службового пакета

        # Сумарний час передачі
        transmission_time = sum(
            self.network[shortest_path[i]][shortest_path[i + 1]]['weight'] for i in range(len(shortest_path) - 1))

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

    def transmit_message_datagram(self, source, destination, message_size):
        # Логіка передачі повідомлення в режимі дейтаграми

        # Отримати найкоротший маршрут від джерела до призначення
        shortest_path = self.transit_paths[source][destination]['path']

        # Розрахувати сумарний час передачі на основі ваги каналу першої ребра
        transmission_time = sum(
            self.network[shortest_path[i]][shortest_path[i + 1]]['weight'] for i in range(len(shortest_path) - 1))

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

    def visualize_network(self):
        pos = nx.spring_layout(self.network, k=1.5)

        # Візуалізація вузлів та робочих станцій
        nx.draw_networkx_nodes(self.network, pos,
                               nodelist=[node for node in self.network.nodes() if int(node) < self.node_count],
                               node_color='blue', node_shape='o')
        nx.draw_networkx_nodes(self.network, pos,
                               nodelist=[node for node in self.network.nodes() if int(node) > self.node_count],
                               node_color='red', node_shape='^')
        # Візуалізація ребер
        nx.draw_networkx_edges(self.network, pos, edge_color='black')
        # if self.transit_paths:
        #     red_edges = []
        #     for path_info in self.transit_paths.values():
        #         path = path_info.get('path', [])  # Use get() to handle the case where 'path' is not present
        #         red_edges.extend([(path[i], path[i + 1]) for i in range(len(path) - 1)])
        #         print(f'Here {red_edges}')
        #
        #     nx.draw_networkx_edges(self.network, pos, edgelist=red_edges, edge_color='red', width=2)

        # Візуалізація міток
        labels = {node: node for node in self.network.nodes()}
        nx.draw_networkx_labels(self.network, pos, labels=labels)

        # Візуалізація ваг ребер
        edge_labels = {(i, j): self.network[i][j]["weight"] for i, j in self.network.edges()}
        nx.draw_networkx_edge_labels(self.network, pos, edge_labels=edge_labels)

        plt.show()

    def display_distance_tables(self, excel_filename="./project_data/distance_tables.xlsx"):
        data = []
        columns = ["Source", "Destination", "Transit Count", "Path", "Edge Weights"]

        for source_workstation in self.workstations:
            source_id = source_workstation['node']
            print(f"Distance Table from Workstation {source_id} to other workstations:")
            for destination_workstation in self.workstations:
                dest_id = destination_workstation['node']
                if source_id != dest_id:
                    path = self.transit_paths[source_id][dest_id]['path']
                    transit_count = self.transit_paths[source_id][dest_id]['transit_count']

                    # Extract edge weights along the path
                    edge_weights = [self.network[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1)]

                    data.append([source_id, dest_id, transit_count, path, edge_weights])

                    print(
                        f"To Workstation {dest_id}, Transit Count: {transit_count}, Path: {path}, Edge Weights: {edge_weights}")
            print('\n')

        df = pd.DataFrame(data, columns=columns)
        df.to_excel(excel_filename, index=False)
        print(f"Distance tables exported to {excel_filename}")

    # Collect and print the statistics
    def collect_statistics(self, transmission_result):
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