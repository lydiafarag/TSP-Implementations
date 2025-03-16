from itertools import permutations
import networkx as nx

def calculate_total_distance(route, graph):
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))

def tsp_brute_force(graph):
    nodes = list(graph.nodes)  

    if len(nodes) == 1:
        return [nodes[0], nodes[0]], 0  

    if not nx.is_connected(graph):
        return None, float('inf')  

    if any(data['weight'] < 0 for _, _, data in graph.edges(data=True)):
        return None, float("inf")

    min_route = None
    min_cost = float('inf')

    for perm in permutations(nodes[1:]):  
        route = [nodes[0]] + list(perm) + [nodes[0]]  
        cost = calculate_total_distance(route, graph)

        if cost < min_cost:
            min_cost = cost
            min_route = route

    return min_route, min_cost
