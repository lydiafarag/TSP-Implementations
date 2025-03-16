import heapq
import networkx as nx

def calculate_total_distance(route, graph):
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))

def tsp_branch_and_bound(graph):
    if len(graph.nodes) == 1:
        return [list(graph.nodes)[0], list(graph.nodes)[0]], 0  

    if not nx.is_connected(graph):
        return None, float('inf')  

    if any(data['weight'] < 0 for _, _, data in graph.edges(data=True)):
        return None, float("inf")

    def lower_bound(path):
        return sum(min(graph[node][neighbor]['weight'] for neighbor in graph.neighbors(node)) for node in path)

    start_node = list(graph.nodes)[0]
    pq = [(0, [start_node])]
    min_cost = float('inf')
    min_route = None

    while pq:
        cost, path = heapq.heappop(pq)

        if len(path) == len(graph) + 1 and path[0] == path[-1]:
            if cost < min_cost:
                min_cost = cost
                min_route = path

        elif len(path) <= len(graph):
            last = path[-1]
            for neighbor in graph.neighbors(last):
                if neighbor not in path or (len(path) == len(graph) and neighbor == path[0]):
                    new_path = path + [neighbor]
                    new_cost = cost + graph[last][neighbor]['weight']

                    if new_cost + lower_bound(new_path) < min_cost:
                        heapq.heappush(pq, (new_cost, new_path))

    return min_route, min_cost
