from itertools import permutations
import networkx as nx


#total distance of a given route in the graph, its the same for all implementations
def calculate_total_distance(route, graph):
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))

def tsp_brute_force(graph):
    nodes = list(graph.nodes)  
    #handles the case of a single node
    if len(nodes) == 1:
        return [nodes[0], nodes[0]], 0  
    ##handles the case of a disconnected graph
    if not nx.is_connected(graph):
        return None, float('inf')  
    ##disallows any negative weights
    if any(data['weight'] < 0 for _, _, data in graph.edges(data=True)):
        return None, float("inf")

    min_route = None
    min_cost = float('inf')
    #try all permutations of the nodes except first one
    for perm in permutations(nodes[1:]):  
        #create the route starting and ending at the first node
        route = [nodes[0]] + list(perm) + [nodes[0]]  
        cost = calculate_total_distance(route, graph)
        #check if the current route is better than the best one found so far
        if cost < min_cost:
            min_cost = cost
            min_route = route

    return min_route, min_cost
