# TSP-Implementations

This project implements and analyzes four different algorithms for solving the **Traveling Salesperson Problem (TSP)**

- **Brute Force**
- **Branch and Bound**
- **Dynamic Programming (Held-Karp)**
- **Approximation Algorithms (MST-Based)**

Then, their respective efficencies and accuracies on different types of graphs is asssed and analyzed. 

## **1. Getting Started**

### **1.1 Prerequisites**
Ensure you have the following installed:
- Python 3.10+
- Required dependencies (install via `pip`):
  ```sh
  pip install -r requirements.txt
  ```

### **1.2 Project Structure**
TSP-IMPLEMENTATIONS/
│── algorithms/            # Implementations of TSP algorithms
│   ├── TSP_bruteforce.py
│   ├── TSP_branch_and_bound.py
│   ├── TSP_DP.py
│   ├── TSP_approx.py
│── datasets/              # Generated graph data
│── results/               # Generated output files (CSV, PNG)
│── main.py                # Runs a single experiment
│── analyze_performance.py # Runs multiple trials & generates performance plots
│── requirements.txt       # Dependencies
│── README.md              # Documentation
│── test_tsp.py            # Test suite for verifying implementations
|── run_custom_test.py     # Python file allowing for custom test to be run

## **2. Running the Implementations**

### 2.1 Running a Single Experiment
You can run **all algorithms** on different graph types using:

```sh
python main.py
```

This generates a results file in the results/ directory. The numbers are randomly generated everytime the script runs. 

### 2.2 Running Multiple Trials and Performance Analysis 

To analyze performance over multiple trials, run 

```sh
python analyze_performance.py
```

This will:
- execute multiple trials for each algorithm 
- store the results in **multiple_trials_results.csv**
- generate runtime plots in results/

### 2.3 Running Custom Tests

To run a a custom test, run the script:
```sh
python run_custom_test.py
```
Next:
1. Enter the number of nodes (N)
2. Enter an edge probability (0.3 for sparse, 1.0 for fully connected)
3. Choose an algorithm (not all apply depending on N)

This script will:
- generate a graph 
- run the selected TSP algorithm 
- print and save the results to results/custom_test_results.csv


## 3. Understanding the Implementations 

### 3.1 Brute Force 
- enumerates all possible routes
- **Time Complexity**: O(n!)
- **Use for**: Very small graphs 

### 3.2 Branch and Bound
- uses pruning to eliminate suboptimal paths
- **Time Complexity**: O(n!) worst case, but O(2^n) average case
- **Use for**: Medium graphs

### 3.3 Dynamic Programming 
- uses top-down memoization to solve subproblems 
- **Time Complexity**: O(2^n) 
- **Use for**: Relatively large graphs (up to N~20)

### 3.4 Approximation Algorithm
- constructs a Minimum Spanning Tree and does preorder  traversal
- garuntees a tour within 2x the optimal tour
- **Time Complexity**: O(n^2)
- **Use for**: Large graphs or graphs with computationally infeasible exact solutions


## 4. Testing Metrics Used

### 4.1 Correctness of Algorithms 

- **Path Validity Check**: The returned path is verified to:
  - Start and end at the same node (forms a cycle).
  - Visit all nodes exactly once before returning to the start.
  - Contain valid edges from the input graph.

- **Comparison Against Expected Optimal Cost**:
  - For small graphs, the Brute Force and Branch & Bound algorithms provide the exact optimal solution.
  - The correctness of **Dynamic Programming (Held-Karp)** is verified by ensuring it returns the same optimal cost as Brute Force.
  - The **Approximation Algorithm** is validated by checking that it produces a finite tour cost.

- **Unit Testing with Pytest**:
  - The test suite (`test_tsp.py`) uses **pytest** to validate each implementation against a known small graph.
  - The expected optimal solution for the test graph is **80**, and the results of each algorithm are compared against this value.
  - The Approximation Algorithm is not expected to return exactly **80** but must return a finite positive value.

### 4.2 Performance of Algorithms 

To evaluate efficiency, the following metrics were recorded:

- **Execution Time**:
  - The runtime of each algorithm was measured over different graph types and sizes.
  - Results were stored in `multiple_trials_results.csv` and visualized as line plots.

- **Scalability Trends**:
  - The **Brute Force** algorithm is expected to scale poorly (factorial complexity).
  - **Branch and Bound** improves performance by pruning suboptimal paths but remains exponential.
  - **Dynamic Programming (Held-Karp)** reduces computation using memoization but still scales exponentially.
  - The **Approximation Algorithm** provides a polynomial-time alternative that sacrifices optimality for speed.

- **Multiple Trials**:
  - Each algorithm was tested across multiple runs on different graph structures to ensure consistency.

Plots of runtime comparisons can be found in the `results/` directory.

## 5. Conclusions & Next Steps:

### 5.1 Summary of Findings: 

From our experiments, we analyzed the performance of **four different TSP algorithms**—Brute Force, Branch and Bound, Dynamic Programming, and an Approximation Algorithm—on various types of graphs. The key takeaways are:

- **Brute Force**: Guarantees an optimal solution but becomes computationally infeasible for graphs larger than **10 nodes** due to factorial growth.
- **Branch and Bound**: Performs significantly better than Brute Force by pruning suboptimal paths but still struggles with larger graphs (**>12 nodes**).
- **Dynamic Programming (Held-Karp Algorithm)**: Achieves better efficiency than brute force by reducing redundant computations but has an **O(2ⁿ * n) complexity**, making it impractical for large graphs.
- **Approximation Algorithm (MST-based)**: Runs efficiently in **O(n² log n)** but does not always guarantee the optimal path. However, it provides a good tradeoff between **speed and accuracy**, particularly on larger graphs.

The **graph structure** played a significant role in algorithm efficiency:
- **Sparse graphs** led to faster runtimes but could impact path accuracy.
- **Fully connected graphs** ensured optimality but significantly increased computational cost.


### 5.2 Future Improvements:

Several improvements can be made to enhance the implementation and performance evaluation:

- **More Advanced Heuristics**: Implementing **Christofides' algorithm** could improve the approximation accuracy while maintaining polynomial time complexity.
- **Parallelization**: Some algorithms (e.g., Branch and Bound) could benefit from parallel computing to prune paths more efficiently.
- **Experimenting on Larger Graphs**: Currently, the analysis is limited to **graphs of 12 nodes**. Future work could explore scaling up using **metaheuristic approaches** like Genetic Algorithms or Simulated Annealing.
- **Hybrid Approaches**: Combining **DP optimizations with approximation methods** could lead to **more scalable** yet **reasonably accurate** solutions.