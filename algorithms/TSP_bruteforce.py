from itertools import permutations

def calculate_total_distance(route, graph):
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))

def tsp_brute_force(graph):
    nodes = list(graph.nodes)
    min_route = None
    min_cost = float('inf')
    for perm in permutations(nodes[1:]):  # Fix first node as start
        route = [nodes[0]] + list(perm) + [nodes[0]]
        cost = calculate_total_distance(route, graph)
        if cost < min_cost:
            min_cost = cost
            min_route = route
    return min_route, min_cost
