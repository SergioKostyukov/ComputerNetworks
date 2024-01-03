def dijkstra_algorithm(graph, start, end):
    # Ініціалізація відстаней та попередників
    distances = {node: float('infinity') for node in graph.nodes}
    predecessors = {node: None for node in graph.nodes}
    distances[start] = 0

    # Створення множини вершин для обробки
    nodes_to_visit = set(graph.nodes)

    while nodes_to_visit:
        # Вибір вершини з найменшою відстанню
        current_node = min(nodes_to_visit, key=lambda node: distances[node])

        # Вихід, якщо досягнута кінцева вершина
        if current_node == end:
            break

        # Оновлення відстаней та попередників для сусідів поточної вершини
        for neighbor in graph.neighbors(current_node):
            potential_route = distances[current_node] + graph[current_node][neighbor]['weight']
            if potential_route < distances[neighbor]:
                distances[neighbor] = potential_route
                predecessors[neighbor] = current_node

        # Видалення поточної вершини з множини для обробки
        nodes_to_visit.remove(current_node)

    # Побудова оптимального шляху
    optimal_path = []
    current_node = end
    while predecessors[current_node] is not None:
        optimal_path.insert(0, current_node)
        current_node = predecessors[current_node]
    optimal_path.insert(0, start)

    return optimal_path, distances[end]
