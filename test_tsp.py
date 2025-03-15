import networkx as nx
import pytest
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

def test_tsp_brute_force(small_graph):
    route, cost = tsp_brute_force(small_graph)
    assert is_valid_tsp_path(small_graph, route)
    assert cost == 80  # Expected optimal solution


def test_tsp_branch_and_bound(small_graph):
    route, cost = tsp_branch_and_bound(small_graph)
    assert is_valid_tsp_path(small_graph, route)
    assert cost == 80  # Expected optimal solution


def test_tsp_dynamic_programming(small_graph):
    route, cost = tsp_dynamic_programming(small_graph)
    assert is_valid_tsp_path(small_graph, route)
    assert cost == 80  # Expected optimal solution


def test_tsp_approximation(small_graph):
    route, cost = tsp_approximation(small_graph)
    assert is_valid_tsp_path(small_graph, route)
    assert cost > 0  # Should return a finite value
