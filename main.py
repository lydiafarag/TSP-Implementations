import networkx as nx
import pandas as pd
import random
import os
import time
import json
import multiprocessing
import matplotlib.pyplot as plt
from tabulate import tabulate
from algorithms.TSP_bruteforce import tsp_brute_force
from algorithms.TSP_branch_and_bound import tsp_branch_and_bound
from algorithms.TSP_DP import tsp_dynamic_programming
from algorithms.TSP_approx import tsp_approximation

DATASET_FOLDER = "datasets"
RESULTS_FOLDER = "results"

os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(DATASET_FOLDER, exist_ok=True)

random.seed(42)

def generate_graph(num_nodes, edge_prob=1.0):
    G = nx.Graph()
    nodes = list(range(num_nodes))

    for i in nodes:
        for j in nodes:
            if i != j and random.random() <= edge_prob:
                G.add_edge(i, j, weight=random.randint(1, 100))

    dataset_path = os.path.join(DATASET_FOLDER, f"graph_{num_nodes}.json")
    with open(dataset_path, "w") as f:
        json.dump(nx.node_link_data(G), f, indent=4)

    return G, dataset_path

def algorithm_runner(queue, algorithm, G):

    try:
        result = algorithm(G)
        queue.put(result)
    except Exception:
        queue.put((None, None))

def run_algorithm_with_timeout(algorithm, G, timeout=60):
    #timeout added to preclude execution infinitely 
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=algorithm_runner, args=(queue, algorithm, G))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        return None, None

    return queue.get()

def run_experiments():
    test_cases = [
        ("Small graph (4 nodes)", generate_graph(4)),
        ("Medium graph (8 nodes)", generate_graph(8)),
        ("Medium graph (10 nodes)", generate_graph(10)),
        ("Large graph (12 nodes)", generate_graph(12)),
        ("Sparse graph (12 nodes, 30% edges)", generate_graph(12, edge_prob=0.3)),
        ("Fully connected (12 nodes)", generate_graph(12, edge_prob=1.0))
    ]

    results = []
    runtime_results = []

    for test_name, (G, dataset_path) in test_cases:
        print(f"\nRunning experiments for: {test_name}...")

        algorithms = [
            ("Brute Force", tsp_brute_force) if len(G.nodes) <= 10 else None,
            ("Branch and Bound", tsp_branch_and_bound) if len(G.nodes) <= 12 else None,
            ("Dynamic Programming", tsp_dynamic_programming),
            ("Approximation Algorithm", tsp_approximation)
        ]

        for algorithm_entry in algorithms:
            if algorithm_entry is None:
                continue

            algorithm_name, algorithm = algorithm_entry
            print(f"  Running {algorithm_name}...")

            start_time = time.time()
            route, cost = run_algorithm_with_timeout(algorithm, G, timeout=60)
            end_time = time.time()
            runtime = end_time - start_time

            results.append({
                "Test Case": test_name,
                "Graph Size": len(G.nodes),
                "Algorithm": algorithm_name,
                "Path": route,
                "Cost": cost,
                "Dataset": dataset_path
            })

            runtime_results.append({
                "Test Case": test_name,
                "Graph Size": len(G.nodes),
                "Algorithm": algorithm_name,
                "Runtime (seconds)": runtime
            })

    results_df = pd.DataFrame(results)
    runtime_df = pd.DataFrame(runtime_results)

    results_path = os.path.join(RESULTS_FOLDER, "results.csv")
    runtime_path = os.path.join(RESULTS_FOLDER, "runtime_analysis.csv")

    results_df.to_csv(results_path, index=False)
    runtime_df.to_csv(runtime_path, index=False)

    print("\nResults saved to:")
    print(f"- {results_path}")
    print(f"- {runtime_path}")

    print("\nTSP Results Summary")
    print(tabulate(results_df, headers="keys", tablefmt="grid"))

    print("\nTSP Runtime Comparison")
    print(tabulate(runtime_df, headers="keys", tablefmt="grid"))

    plot_runtime_per_test_case(runtime_df)

def plot_runtime_per_test_case(runtime_df):
    algorithm_colors = {
        "Brute Force": "blue",
        "Branch and Bound": "orange",
        "Dynamic Programming": "green",
        "Approximation Algorithm": "red"
    }
    algorithm_acronyms = {
        "Brute Force": "BF",
        "Branch and Bound": "B&B",
        "Dynamic Programming": "DP",
        "Approximation Algorithm": "Approx"
    }
    for test_case in runtime_df["Test Case"].unique():
        subset = runtime_df[runtime_df["Test Case"] == test_case]

        plt.figure(figsize=(8, 5))
        bar_colors = [algorithm_colors.get(alg, "gray") for alg in subset["Algorithm"]]
        x_labels = [algorithm_acronyms.get(alg, alg) for alg in subset["Algorithm"]]

        plt.bar(x_labels, subset["Runtime (seconds)"], color=bar_colors)
        plt.xlabel("Algorithm")
        plt.ylabel("Runtime (seconds)")
        plt.title(f"TSP Runtime for {test_case}")
        plt.xticks(rotation=30, ha="right")

        plot_path = os.path.join(RESULTS_FOLDER, f"runtime_{test_case.replace(' ', '_')}.png")
        plt.savefig(plot_path)
        plt.show()

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")  # Needed for Windows
    run_experiments()
