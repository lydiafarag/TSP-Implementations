import networkx as nx

def calculate_total_distance(route, graph):
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))

def tsp_dynamic_programming(graph):
    nodes = list(graph.nodes)
    n = len(nodes)

    if n == 1:
        return [nodes[0], nodes[0]], 0  

    if not nx.is_connected(graph):
        return None, float('inf')  

    if any(data['weight'] < 0 for _, _, data in graph.edges(data=True)):
        return None, float("inf")

    dist = {i: {j: float('inf') for j in range(n)} for i in range(n)}
    for u, v, data in graph.edges(data=True):
        i, j = nodes.index(u), nodes.index(v)
        dist[i][j] = data['weight']
        dist[j][i] = data['weight']  

    memo = {}

    def visit(mask, last):
        if mask == (1 << n) - 1:  
            return dist[last][0]  

        if (mask, last) in memo:  
            return memo[(mask, last)]

        min_cost = float('inf')
        for next_node in range(n):
            if mask & (1 << next_node) == 0: 
                cost = dist[last][next_node] + visit(mask | (1 << next_node), next_node)
                min_cost = min(min_cost, cost)

        memo[(mask, last)] = min_cost
        return min_cost

    min_cost = visit(1, 0)

    path = [0]
    mask = 1
    last = 0

    while len(path) < n:
        best_next = None
        for next_node in range(n):
            if mask & (1 << next_node) == 0:  
                expected_cost = visit(mask | (1 << next_node), next_node) + dist[last][next_node]
                if expected_cost == min_cost:
                    best_next = next_node
                    min_cost -= dist[last][next_node]
                    break
        
        if best_next is None:
            return None, float('inf')

        path.append(best_next)
        mask |= (1 << best_next)
        last = best_next

    path.append(0)  

    return path, calculate_total_distance(path, graph)
