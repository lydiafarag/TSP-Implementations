import networkx as nx
import random
import json
import os
import time
import pandas as pd
from algorithms.TSP_bruteforce import tsp_brute_force
from algorithms.TSP_branch_and_bound import tsp_branch_and_bound
from algorithms.TSP_DP import tsp_dynamic_programming
from algorithms.TSP_approx import tsp_approximation

DATASET_FOLDER = "datasets"
RESULTS_FOLDER = "results"

os.makedirs(DATASET_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def generate_custom_graph(num_nodes, edge_prob):
    """Generates a weighted graph for TSP based on user input."""
    G = nx.Graph()
    nodes = list(range(num_nodes))

    for i in nodes:
        for j in nodes:
            if i != j and random.random() <= edge_prob:
                G.add_edge(i, j, weight=random.randint(1, 100))

    dataset_path = os.path.join(DATASET_FOLDER, f"custom_graph_{num_nodes}.json")
    with open(dataset_path, "w") as f:
        json.dump(nx.node_link_data(G), f, indent=4)

    return G, dataset_path

def run_custom_test():
    """Allows user to input custom values and run a TSP test."""
    print("\n📌 **Custom TSP Test Runner**\n")
    
    # Get user inputs
    num_nodes = int(input("Enter the number of nodes (e.g., 4-12): "))
    edge_prob = float(input("Enter edge probability (0.1 = sparse, 1.0 = fully connected): "))

    # Validate inputs
    if num_nodes < 4:
        print("⚠️ Number of nodes must be at least 4.")
        return
    
    if not (0 < edge_prob <= 1):
        print("⚠️ Edge probability must be between 0 and 1.")
        return

    algorithms = {
        "1": ("Brute Force", tsp_brute_force) if num_nodes <= 10 else None,
        "2": ("Branch and Bound", tsp_branch_and_bound) if num_nodes <= 12 else None,
        "3": ("Dynamic Programming", tsp_dynamic_programming),
        "4": ("Approximation Algorithm", tsp_approximation)
    }
    
    print("\n📌 Select an Algorithm:")
    for key, algo in algorithms.items():
        if algo:
            print(f"  {key}. {algo[0]}")
    
    algo_choice = input("\nEnter the number corresponding to the algorithm: ")
    
    if algo_choice not in algorithms or not algorithms[algo_choice]:
        print("⚠️ Invalid choice or algorithm not applicable for the given number of nodes.")
        return

    algorithm_name, algorithm_func = algorithms[algo_choice]

    # Generate Graph
    print("\n🔄 Generating graph...")
    G, dataset_path = generate_custom_graph(num_nodes, edge_prob)
    print(f"✅ Graph generated and saved to {dataset_path}")

    # Run Algorithm
    print(f"\n🚀 Running {algorithm_name} algorithm...")
    start_time = time.time()
    route, cost = algorithm_func(G)
    end_time = time.time()
    runtime = end_time - start_time

    # Display Results
    print("\n🎯 **Results:**")
    print(f"  ➤ Algorithm: {algorithm_name}")
    print(f"  ➤ Path: {route}")
    print(f"  ➤ Cost: {cost}")
    print(f"  ➤ Execution Time: {runtime:.4f} seconds")

    # Save to CSV
    results_path = os.path.join(RESULTS_FOLDER, "custom_test_results.csv")
    results_df = pd.DataFrame([{
        "Graph Size": num_nodes,
        "Edge Probability": edge_prob,
        "Algorithm": algorithm_name,
        "Path": route,
        "Cost": cost,
        "Runtime (seconds)": runtime
    }])
    
    results_df.to_csv(results_path, mode='a', index=False, header=not os.path.exists(results_path))
    print(f"\n📁 Results saved to `{results_path}`")

if __name__ == "__main__":
    run_custom_test()
