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

        # Generate workstation nodes with unique IDs
        self.workstations = []  # Clear the list before populating
        for i in range(len(self.workstationid)):
            self.node_count += 1
            workstation_id = self.node_count - 1
            weight = random.choice(self.channels)
            self.network.add_node(workstation_id)
            self.network.add_edge(workstation_id, self.workstationid[i], weight=weight, type=chtype)
            self.workstations.append({"id": workstation_id, "node": self.workstationid[i], "channel_type": chtype,
                                      "channel_weight": weight})

        # Additional logic to add two edges with type "SIMPLEX"
        simplex_edges = list(itertools.combinations(range(self.node_count), 2))[:2]
        for edge in simplex_edges:
            self.network.add_edge(edge[0], edge[1], weight=random.choice(self.channels), type="SIMPLEX")

    def save_configuration(self, filename="./project_data/network_config.json"):
        self.save_network()
        self.save_workstations()

        data = {
            "network": nx.to_dict_of_dicts(self.network),
            "workstations": self.workstations
        }
        with open(filename, "w") as file:
            json.dump(data, file)

    def save_network(self, filename="./project_data/network.xlsx"):
        graph_data = {'Node 1': [], 'Node 2': [], 'Weight': [], 'Type': []}

        for edge in self.network.edges(data=True):
            graph_data['Node 1'].append(edge[0])
            graph_data['Node 2'].append(edge[1])
            graph_data['Weight'].append(edge[2]['weight'])
            graph_data['Type'].append(edge[2]['type'])

        graph_df = pd.DataFrame(graph_data)
        graph_df.to_excel(filename, sheet_name='Graph Info', index=False)

        print(f"Network information exported to {filename}")

    def save_workstations(self, filename="./project_data/workstations.xlsx"):
        channels_data = {'ID': [], 'Node': [], 'Channel Type': [], 'Channel Weight': []}

        for workstation in self.workstations:
            channels_data['ID'].append(workstation['id'])
            channels_data['Node'].append(workstation['node'])
            channels_data['Channel Type'].append(workstation['channel_type'])
            channels_data['Channel Weight'].append(workstation['channel_weight'])

        channels_df = pd.DataFrame(channels_data)
        channels_df.to_excel(filename, sheet_name='Channels Info', index=False)

        print(f"Workstations information exported to {filename}")

    def load_configuration(self, filename="./project_data/network_config.json"):
        with open(filename, "r") as file:
            data = json.load(file)
            self.network = nx.DiGraph(data["network"])
            self.workstations = data["workstations"]

    def visualize_network(self):
        pos = nx.spring_layout(self.network, k=1.5)

        # Візуалізація вузлів та робочих станцій
        nx.draw_networkx_nodes(self.network, pos,
                               nodelist=[node for node in self.network.nodes() if int(node) < 24],
                               node_color='blue', node_shape='o')
        nx.draw_networkx_nodes(self.network, pos,
                               nodelist=[node for node in self.network.nodes() if int(node) >= 24],
                               node_color='red', node_shape='^')
        # Візуалізація ребер
        nx.draw_networkx_edges(self.network, pos, edge_color='black')

        # Візуалізація міток
        labels = {node: node for node in self.network.nodes()}
        nx.draw_networkx_labels(self.network, pos, labels=labels)

        # Візуалізація ваг ребер
        edge_labels = {(i, j): self.network[i][j]["weight"] for i, j in self.network.edges()}
        nx.draw_networkx_edge_labels(self.network, pos, edge_labels=edge_labels)

        plt.show()

    def save_distance_table(self, excel_filename="./project_data/distance_tables.xlsx"):
        data = []
        columns = ["Source", "Destination", "Transit Count", "Path", "Edge Weights"]

        workstations_ids = [workstation['id'] for workstation in self.workstations]

        for source_id in workstations_ids:
            print(f"Distance Table from Workstation {source_id} to other workstations:")
            for dest_id in workstations_ids:
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
