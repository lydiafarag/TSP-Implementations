import networkx as nx
import numpy as np


def calculate_total_distance(route, graph):
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))



def tsp_approximation(graph):
    def preorder_traversal(tree, node, visited):
        visited.append(node)
        for neighbor in sorted(tree.neighbors(node)):
            if neighbor not in visited:
                preorder_traversal(tree, neighbor, visited)
    
    start_node = list(graph.nodes)[0]
    mst = nx.minimum_spanning_tree(graph)
    preorder_list = []
    preorder_traversal(mst, start_node, preorder_list)
    preorder_list.append(preorder_list[0])
    return preorder_list, calculate_total_distance(preorder_list, graph)

if __name__ == "__main__":
    G = nx.Graph()
    edges = [
        ("A", "B", 10), ("A", "C", 15), ("A", "D", 20),
        ("B", "C", 35), ("B", "D", 25),
        ("C", "D", 30)
    ]
    
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    