import networkx as nx
import pytest
import time # For timeouts
from algorithms.TSP_bruteforce import tsp_brute_force
from algorithms.TSP_branch_and_bound import tsp_branch_and_bound
from algorithms.TSP_DP import tsp_dynamic_programming
from algorithms.TSP_approx import tsp_approximation


def is_valid_tsp_path(graph, path):
    if path is None:
        return False
    if len(path) != len(graph.nodes) + 1:  # Should visit all nodes & return to start
        return False
    if path[0] != path[-1]:  # Must start and end at the same node
        return False
    return len(set(path[:-1])) == len(graph.nodes)  # No duplicates except return to start


@pytest.fixture
def small_graph():
    G = nx.Graph()
    edges = [
        (0, 1, 10), (0, 2, 15), (0, 3, 20),
        (1, 2, 35), (1, 3, 25),
        (2, 3, 30)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G


@pytest.fixture
def large_graph():
    G = nx.complete_graph(8)
    for u, v in G.edges():
        G[u][v]['weight'] = (u + v) * 5  # Assign deterministic weights
    return G

@pytest.fixture
def equal_weight_graph():
    G = nx.complete_graph(5)
    for u, v in G.edges():
        G[u][v]['weight'] = 50  # All edges have the same weight
    return G

@pytest.fixture
def single_node_graph():
    G = nx.Graph()
    G.add_node(0)
    return G


@pytest.fixture
def disconnected_graph():
    G = nx.Graph()
    G.add_edges_from([(0, 1, {'weight': 10}), (2, 3, {'weight': 20})])  # Two separate components
    return G

@pytest.fixture
def negative_weight_graph():
    G = nx.complete_graph(5)
    for u, v in G.edges():
        G[u][v]['weight'] = -abs(u - v)  # Assign small negative weights
    return G

@pytest.fixture
def very_large_graph():
    """Creates an even larger graph (n=12) where Branch and Bound may timeout."""
    G = nx.complete_graph(12)
    for u, v in G.edges():
        G[u][v]['weight'] = (u + v) * 5  # Assign deterministic weights
    return G
#tests on small graphs 

@pytest.mark.parametrize("graph", ["small_graph", "large_graph", "equal_weight_graph"])
def test_tsp_dynamic_programming(request, graph):
    G = request.getfixturevalue(graph)
    route, cost = tsp_dynamic_programming(G)
    assert is_valid_tsp_path(G, route)
    assert cost > 0  # Should return a finite value

@pytest.mark.parametrize("graph", ["small_graph", "large_graph", "equal_weight_graph"])
def test_tsp_approximation(request, graph):
    G = request.getfixturevalue(graph)
    route, cost = tsp_approximation(G)
    assert is_valid_tsp_path(G, route)
    assert cost > 0  # Should return a finite value

# single Node Graph (TSP Should Return Trivial Tour)
@pytest.mark.parametrize("algorithm", [tsp_brute_force, tsp_branch_and_bound, tsp_dynamic_programming, tsp_approximation])
def test_single_node_graph(algorithm, single_node_graph):
    route, cost = algorithm(single_node_graph)
    assert route == [0, 0]  # Only one node, must return to itself
    assert cost == 0  # No distance to travel
#  Disconnected Graph (TSP Should Return No Path)
@pytest.mark.parametrize("algorithm", [tsp_brute_force, tsp_branch_and_bound, tsp_dynamic_programming, tsp_approximation])
def test_disconnected_graph(algorithm, disconnected_graph):
    route, cost = algorithm(disconnected_graph)
    assert route is None  # No valid path should exist
    assert cost == float("inf")  # Cost should be infinite


@pytest.mark.parametrize("algorithm", [tsp_brute_force, tsp_branch_and_bound, tsp_dynamic_programming, tsp_approximation])
def test_negative_weight_graph(algorithm, negative_weight_graph):
    route, cost = algorithm(negative_weight_graph)
    assert route is None and cost==float("inf")  # No valid path should exist
    

@pytest.mark.timeout(5)  # Set a 5-second timeout
def test_brute_force_timeout(large_graph):
    start_time = time.time()
    route, cost = tsp_brute_force(large_graph)
    end_time = time.time()
    assert end_time - start_time < 5, "Brute Force took too long!"
    
