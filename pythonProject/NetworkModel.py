import networkx as nx
import matplotlib.pyplot as plt
import random
import json
import itertools


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

    def save_configuration(self, filename):
        data = {
            "network": nx.to_dict_of_dicts(self.network),
            "workstations": self.workstations
        }
        with open(filename, "w") as file:
            json.dump(data, file)

    def load_configuration(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            self.network = nx.DiGraph(data["network"])
            self.workstations = data["workstations"]

    def visualize_network(self):
        pos = nx.spring_layout(self.network, k=1.5)

        # Візуалізація вузлів та робочих станцій
        nx.draw_networkx_nodes(self.network, pos,
                               nodelist=[node for node in self.network.nodes() if node < self.node_count],
                               node_color='blue', node_shape='o')
        nx.draw_networkx_nodes(self.network, pos,
                               nodelist=[node for node in self.network.nodes() if node > self.node_count],
                               node_color='red', node_shape='^')
        # Візуалізація ребер
        nx.draw_networkx_edges(self.network, pos)

        # Візуалізація міток
        labels = {node: node for node in self.network.nodes()}
        nx.draw_networkx_labels(self.network, pos, labels=labels)

        # Візуалізація ваг ребер
        edge_labels = {(i, j): self.network[i][j]["weight"] for i, j in self.network.edges()}
        nx.draw_networkx_edge_labels(self.network, pos, edge_labels=edge_labels)

        plt.show()

    def find_shortest_paths(self):
        paths = {}
        for workstation in self.workstations:
            paths[workstation] = {}
            for destination in range(self.node_count):
                if workstation != destination:
                    shortest_path = nx.shortest_path(self.network, source=workstation, target=destination,
                                                     weight="weight")
                    total_weight = sum(self.network[shortest_path[i]][shortest_path[i + 1]]["weight"] for i in
                                       range(len(shortest_path) - 1))
                    paths[workstation][destination] = {"path": shortest_path, "weight": total_weight}
        return paths

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

    def display_distance_tables(self):
        for source_workstation in self.workstations:
            source_id = source_workstation['node']
            print(f"Distance Table from Workstation {source_id} to other workstations:")
            for destination_workstation in self.workstations:
                dest_id = destination_workstation['node']
                if source_id != dest_id:
                    transit_count = self.transit_paths[source_id][dest_id]['transit_count']
                    print(f"To Workstation {dest_id}, Transit Count: {transit_count}")
            print("\n")
