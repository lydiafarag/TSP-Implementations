import numpy as np

def calculate_total_distance(route, graph):
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))

# Dynamic programming solution to the TSP:
#     # we take in the route(list) of the cities in the order they are visited
#     # we take in the graph(networkx graph) of the cities and the distances between them
#     # we use the  Held-Karp algorithm to solve the TSP using DP and return the minimum route and the cost of the minimum route and the result is a tuple with the best route as a list and the minimum cost given as an integer

def tsp_dynamic_programming(graph):
    nodes = list(graph.nodes) # List of nodes in the graph (ie all of the cities)
    n = len(nodes)
    dp = {}  # (bitmask, current_node) -> cost, parent
    
    for i in range(n):
        dp[(1 << i, i)] = (0, None)
    
    for mask in range(1, 1 << n):
        for i in range(n):
            if not (mask & (1 << i)):
                continue
            for j in range(n):
                if mask & (1 << j) or i == j:
                    continue
                prev_mask = mask ^ (1 << i)
                new_cost = dp.get((prev_mask, j), (float('inf'), None))[0] + graph[nodes[j]][nodes[i]]['weight']
                if (mask, i) not in dp or new_cost < dp[(mask, i)][0]:
                    dp[(mask, i)] = (new_cost, j)
    
    min_cost = float('inf')
    min_route = []
    last = None
    
    mask = (1 << n) - 1
    for i in range(n):
        cost, parent = dp.get((mask, i), (float('inf'), None))
        if cost < min_cost:
            min_cost = cost
            last = i
    
    if last is None:
        return None, float('inf')
    
    while last is not None:
        min_route.append(nodes[last])
        mask ^= (1 << last)
        last = dp[(mask | (1 << last), last)][1]
    
    min_route.append(min_route[0])
    return list(reversed(min_route)), min_cost
