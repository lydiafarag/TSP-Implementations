import networkx as nx

def calculate_total_distance(route, graph):
    """Calculates the total distance of a given route."""
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))

def tsp_dynamic_programming(graph):
    nodes = list(graph.nodes)
    n = len(nodes)
    
    # Convert graph into adjacency dictionary for faster lookups
    dist = {i: {j: float('inf') for j in range(n)} for i in range(n)}
    for u, v, data in graph.edges(data=True):
        i, j = nodes.index(u), nodes.index(v)
        dist[i][j] = data['weight']
        dist[j][i] = data['weight']  # Undirected graph

    memo = {}  # Dictionary-based memoization

    def visit(mask, last):
        #Recursively finds the shortest TSP route using DP + Memoizatio
        if mask == (1 << n) - 1:  
            return dist[last][0]  

        if (mask, last) in memo:  # check memoized results
            return memo[(mask, last)]

        min_cost = float('inf')
        for next_node in range(n):
            if mask & (1 << next_node) == 0: 
                cost = dist[last][next_node] + visit(mask | (1 << next_node), next_node)
                min_cost = min(min_cost, cost)

        memo[(mask, last)] = min_cost
        return min_cost

    
    min_cost = visit(1, 0)

    #Path Reconstruction
    path = [0]
    mask = 1
    last = 0

    while len(path) < n:
        best_next = None
        for next_node in range(n):
            if mask & (1 << next_node) == 0:  # If not visited
                expected_cost = visit(mask | (1 << next_node), next_node) + dist[last][next_node]
                if expected_cost == min_cost:
                    best_next = next_node
                    min_cost -= dist[last][next_node]
                    break
        
        if best_next is None:
            print("Error reconstructing path!")
            return None, float('inf')

        path.append(best_next)
        mask |= (1 << best_next)
        last = best_next

    path.append(0)  # Complete the cycle

    return path, calculate_total_distance(path, graph)
