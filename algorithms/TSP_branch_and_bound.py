import heapq
def calculate_total_distance(route, graph):
    return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))

# Branch and bound solution to the TSP:
#     # we take in the route(list) of the cities in the order they are visited
#the lower bound fucntion is used to give a lower bound estimate for a given path--> the bound is calcualted by summing the minimum edge weight  for the node 
# often, the lower bound is used to prune the search space by eliminating paths that are guaranteed to be suboptimal


def tsp_branch_and_bound(graph):
    def lower_bound(path):
        return sum(min(graph[node][neighbor]['weight'] for neighbor in graph.neighbors(node)) for node in path)
    
    start_node = list(graph.nodes)[0]
    pq = [(0, [start_node])]
    min_cost = float('inf')
    min_route = None
    while pq:
        cost, path = heapq.heappop(pq)
        if len(path) == len(graph) + 1 and path[0] == path[-1]:
            if cost < min_cost:
                min_cost = cost
                min_route = path
        elif len(path) <= len(graph):
            last = path[-1]
            for neighbor in graph.neighbors(last):
                if neighbor not in path or (len(path) == len(graph) and neighbor == path[0]):
                    new_path = path + [neighbor]
                    new_cost = cost + graph[last][neighbor]['weight']
                    if new_cost + lower_bound(new_path) < min_cost:
                        heapq.heappush(pq, (new_cost, new_path))
    return min_route, min_cost