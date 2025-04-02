import heapq
import networkx as nx

#this function calculates the total distance of a given route in the graph, its the same for all implementations
def calculate_total_distance(route, graph):
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))

def tsp_branch_and_bound(graph):
    #handles the case of a single node
    if len(graph.nodes) == 1:
        return [list(graph.nodes)[0], list(graph.nodes)[0]], 0  
    #checks if disconnected and returns NOone
    if not nx.is_connected(graph):
        return None, float('inf')  
    #disallows any negative weights
    if any(data['weight'] < 0 for _, _, data in graph.edges(data=True)):
        return None, float("inf")
    ##this function calculates the lower bound of a given path
    def lower_bound(path):
        return sum(min(graph[node][neighbor]['weight'] for neighbor in graph.neighbors(node)) for node in path)

    start_node = list(graph.nodes)[0]
    #the PQ is initialized with the starting node and a cost of 0 and it stores the paths that are to be explored
    pq = [(0, [start_node])]
    # track the shortest tour found
    min_cost = float('inf')
    min_route = None
    #explore paths until the PQ is empty
    while pq:
        cost, path = heapq.heappop(pq)

        #if the path is complete and returns to the starting node, we check if its the best one found so far
        if len(path) == len(graph) + 1 and path[0] == path[-1]:
            if cost < min_cost:
                min_cost = cost
                min_route = path
        #if the path is not complete, we explore its neighbors
        elif len(path) <= len(graph):
            last = path[-1]
            for neighbor in graph.neighbors(last):
                if neighbor not in path or (len(path) == len(graph) and neighbor == path[0]):
                    new_path = path + [neighbor]
                    new_cost = cost + graph[last][neighbor]['weight']
                    #apply the bounding condition to prune the search space and know if its worth exploring the new path
                    #if the new cost + the lower bound of the new path is less than the current minimum cost, we explore it
                    if new_cost + lower_bound(new_path) < min_cost:
                        heapq.heappush(pq, (new_cost, new_path))

    return min_route, min_cost
