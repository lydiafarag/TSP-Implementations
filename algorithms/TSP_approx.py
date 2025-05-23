import networkx as nx
import numpy as np

#this function calculates the total distance of a given route in the graph, its the same for all implementations
def calculate_total_distance(route, graph):
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))

def tsp_approximation(graph):
    #handles the case of a single node
    if len(graph.nodes) == 1:
        return list(graph.nodes) + list(graph.nodes), 0  
    ##handles the case of a disconnected graph
    if not nx.is_connected(graph):
        return None, float('inf')  
    ##disallows any negative weights
    if any(data['weight'] < 0 for _, _, data in graph.edges(data=True)):
        return None, float("inf")
    ##this function calculates the minimum spanning tree of the graph and returns a preorder traversal of it
    def preorder_traversal(tree, node, visited):
        visited.append(node)
        for neighbor in sorted(tree.neighbors(node)):
            if neighbor not in visited:
                preorder_traversal(tree, neighbor, visited)
    #pick the first node as the starting point 
    start_node = list(graph.nodes)[0]
    mst = nx.minimum_spanning_tree(graph)
    preorder_list = []
    #create a preorder traversal of the minimum spanning tree
    preorder_traversal(mst, start_node, preorder_list)
    preorder_list.append(preorder_list[0])
    
    return preorder_list, calculate_total_distance(preorder_list, graph)



#example usage for testing purposes
if __name__ == "__main__":
    G = nx.Graph()
    edges = [
        ("A", "B", 10), ("A", "C", 15), ("A", "D", 20),
        ("B", "C", 35), ("B", "D", 25),
        ("C", "D", 30)
    ]
    
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    route, cost = tsp_approximation(G)
    print(f"Approximate TSP route: {route}")
    print(f"Approximate TSP cost: {cost}")
