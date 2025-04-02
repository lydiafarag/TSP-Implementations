import networkx as nx


#this function calculates the total distance of a given route in the graph, its the same for all implementations
def calculate_total_distance(route, graph):
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))

def tsp_dynamic_programming(graph):
    # convert the graph to a list for better indexing 
    nodes = list(graph.nodes)
    n = len(nodes)

    #handles the case of a single node
    if n == 1:
        return [nodes[0], nodes[0]], 0  
    #handles the case of a disconnected graph
    if not nx.is_connected(graph):
        return None, float('inf')  
    #disallows any negative weights
    #this is important for the dynamic programming approach to work correctly
    if any(data['weight'] < 0 for _, _, data in graph.edges(data=True)):
        return None, float("inf")
    #distance matrix initialization which stores the weights of the edges
    dist = {i: {j: float('inf') for j in range(n)} for i in range(n)}
    for u, v, data in graph.edges(data=True):
        i, j = nodes.index(u), nodes.index(v)
        dist[i][j] = data['weight']
        dist[j][i] = data['weight']  

    memo = {}
    #recursive function to calculate the minimum cost of visiting all nodes
    def visit(mask, last):
        if mask == (1 << n) - 1:  
            return dist[last][0]  

        if (mask, last) in memo:  
            return memo[(mask, last)]
        #try all unique nodes that have not been visited yet
        min_cost = float('inf')
        for next_node in range(n):
            if mask & (1 << next_node) == 0: 
                cost = dist[last][next_node] + visit(mask | (1 << next_node), next_node)
                min_cost = min(min_cost, cost)

        memo[(mask, last)] = min_cost
        return min_cost
    #start the recursion with the first node visited and no other nodes visited
    min_cost = visit(1, 0)
    
    path = [0]
    mask = 1
    last = 0

    while len(path) < n:
        best_next = None
        for next_node in range(n):
            if mask & (1 << next_node) == 0:  
                #calculate the expected cost of visiting the next node
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
    #calculate the total distance of the path
    return path, calculate_total_distance(path, graph)
