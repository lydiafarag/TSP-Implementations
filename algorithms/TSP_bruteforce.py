from itertools import permutations

def calculate_total_distance(route, graph):
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))

# Brute force solution to the TSP:
    # we take in the route(list) of the cities in the order they are visited
    # we take in the graph(networkx graph) of the cities and the distances between them
    # we return the minimum route and the cost of the minimum route and the result is a tuple with the best route as a list and the minimum cost given as an integer


def tsp_brute_force(graph):
    nodes = list(graph.nodes) # List of nodes in the graph (ie all of the cities)
    min_route = None #initialize the smallest route as being none
    min_cost = float('inf') #start with an infinitely large cost

    for perm in permutations(nodes[1:]):  # fix first node as startin point
        # for each permutation of the nodes starting from the second node, compute the round trup and then update if the newer path is shorter
        route = [nodes[0]] + list(perm) + [nodes[0]]
        cost = calculate_total_distance(route, graph)
        if cost < min_cost:
            min_cost = cost
            min_route = route
    return min_route, min_cost
