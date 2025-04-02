import networkx as nx
import pandas as pd
import random
import os
import time
import json
import multiprocessing
import matplotlib.pyplot as plt
from algorithms.TSP_bruteforce import tsp_brute_force
from algorithms.TSP_branch_and_bound import tsp_branch_and_bound
from algorithms.TSP_DP import tsp_dynamic_programming
from algorithms.TSP_approx import tsp_approximation

# Directory setup
DATASET_FOLDER = "datasets"
RESULTS_FOLDER = "results"

os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(DATASET_FOLDER, exist_ok=True)

random.seed(42)
# This is the number of trials for each algorithm on each graph
NUM_TRIALS = 5  

#function to generate a graph with a given number of nodes and edge probability, does so randomly
#result is saved to JSON file in the datasets folder and then returned
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
#   #function to run the algorithm in a separate process to avoid blocking the main thread
def algorithm_runner(queue, algorithm, G):

    try:
        result = algorithm(G)
        queue.put(result)
    except Exception:
        queue.put((None, None))

#function to run the algorithm with a timeout, if it takes too long it will be terminated

def run_algorithm_with_timeout(algorithm, G, timeout=60):

    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=algorithm_runner, args=(queue, algorithm, G))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        return None, None

    return queue.get()
#function to run the experiments, it generates different graphs and runs the algorithms on them
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
    runtime_results = {}
    


    for test_name, (G, dataset_path) in test_cases:
        runtime_results[test_name] = {algo: [] for algo in ["BF", "B&B", "DP", "Approx Algo"]}
        print(f"\nRunning experiments for: {test_name}...")

        algorithms = [
            ("BF", tsp_brute_force) if len(G.nodes) <= 10 else None,
            ("B&B", tsp_branch_and_bound) if len(G.nodes) <= 12 else None,
            ("DP", tsp_dynamic_programming),
            ("Approx Algo", tsp_approximation)
        ]

        for algorithm_entry in algorithms:
            if algorithm_entry is None:
                continue

            algorithm_name, algorithm = algorithm_entry

            for trial in range(NUM_TRIALS):  
                print(f"  Running {algorithm_name} (Trial {trial+1})...")

                start_time = time.time()
                route, cost = run_algorithm_with_timeout(algorithm, G, timeout=60)
                end_time = time.time()
                runtime = end_time - start_time

                results.append({
                    "Test Case": test_name,
                    "Graph Size": len(G.nodes),
                    "Algorithm": algorithm_name,
                    "Trial": trial + 1,
                    "Path": route,
                    "Cost": cost,
                    "Dataset": dataset_path
                })

                if cost is not None and cost != float('inf'):
                    runtime_results[test_name][algorithm_name].append(runtime)

    results_df = pd.DataFrame(results)
    results_path = os.path.join(RESULTS_FOLDER, "multiple_trials_results.csv")
    results_df.to_csv(results_path, index=False)

    print("\nResults saved to:")
    print(f"- {results_path}")

    plot_performance(runtime_results)

def plot_performance(runtime_results):
  
    ALGORITHM_COLORS = {
    "BF": "blue",
    "B&B": "green",
    "DP": "red",
    "Approx Algo": "purple"
}
    # plot the individual testing plots
    for test_case, algo_runtimes in runtime_results.items():
        plt.figure(figsize=(8, 5))

        for algorithm, runtimes in algo_runtimes.items():
            if runtimes:
                avg_runtime = [sum(runtimes[:i+1]) / (i+1) for i in range(len(runtimes))]  # Cumulative avg
                color = ALGORITHM_COLORS.get(algorithm, None)
                plt.plot(range(1, len(avg_runtime)+1), avg_runtime, marker='o', label=algorithm, color=color)

        plt.xlabel("Trial")
        plt.ylabel("Runtime (seconds)")
        plt.title(f"TSP Algorithm Performance Over Trials ({test_case})")
        plt.legend()
        plt.grid(True)

        plot_path = os.path.join(RESULTS_FOLDER, f"linegraph_{test_case.replace(' ', '_')}.png")
        plt.savefig(plot_path)
        plt.show()

    # overall plot 
    plt.figure(figsize=(10, 6))
    colors = ['b', 'g', 'r', 'c']
    for idx, (test_case, algo_runtimes) in enumerate(runtime_results.items()):
        for algo_idx, (algorithm, runtimes) in enumerate(algo_runtimes.items()):
            if runtimes:
                avg_runtime = [sum(runtimes[:i+1]) / (i+1) for i in range(len(runtimes))]
                color = ALGORITHM_COLORS.get(algorithm, None)
                plt.plot(range(1, len(avg_runtime)+1), avg_runtime, marker='o', linestyle='-',
                         label=f"{algorithm} ({test_case})", color=color)

    plt.xlabel("Trial")
    plt.ylabel("Runtime (seconds)")
    plt.title("TSP Algorithm Performance Across All Graphs")
    plt.legend()
    plt.grid(True)

    summary_plot_path = os.path.join(RESULTS_FOLDER, "summary_runtime_comparison.png")
    plt.savefig(summary_plot_path)
    print(f"\n Summary runtime comparison saved to: {summary_plot_path}")
    plt.show()

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")  # doesnt work on windows without this 
    run_experiments()
