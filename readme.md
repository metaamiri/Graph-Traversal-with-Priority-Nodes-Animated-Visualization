# 📌 Final Algorithm Project — Graph Traversal with Priority Nodes & Animated Visualization

This project is a final submission for the university algorithm course. It demonstrates shortest-path traversal on a randomly generated undirected weighted graph, prioritizing certain nodes, and visualizing the traversal step by step using Matplotlib widgets.

## 🧠 Project Overview

The program generates a graph with:

- Random number of nodes (between 5 and 10)
- Weighted edges with values between 1 and 20
- Each node having a random number of edges within a specified range

## Then it:

1. Selects a set of priority nodes.
2. Starts from a random node.
3. Visits all priority nodes first using Dijkstra's algorithm.
4. Continues visiting all remaining nodes with minimal total cost.
5. Records and exports all paths and metrics into a CSV file.
6. Provides an interactive animation to visualize the traversal process step-by-step.

## 📊 Sample Output (Console)

```bash
Priority nodes: [1, 4, 0]
Start node: 3
Shortest path from node 3 to priority node 0: [3, 0] with shortest distance 17 , visit time unil now : 0.5 and with road time : 0.3
Shortest path from node 0 to priority node 4: [0, 4] with shortest distance 3 , visit time unil now : 1.0 and with road time : 0.1
Shortest path from node 4 to priority node 1: [4, 2, 1] with shortest distance 20 , visit time unil now : 1.5 and with road time : 0.3
Shortest path from node 1 to node 5: [1, 5] with shortest distance 3 , visit time unil now : 2.0 and with road time : 0.1
Shortest path from node 5 to node 2: [5, 1, 2] with shortest distance 12 , visit time unil now : 2.5 and with road time : 0.2
Shortest path from node 2 to node 3: [2, 3] with shortest distance 20 , visit time unil now : 3.0 and with road time : 0.3
Total distance to visit all nodes: 75
Time spent visiting all nodes: 3.0 hours
Time on road : 1.2 hours
Total time spent visiting and riding : 4.2 hours
Average time to fill each atm : 0.7
Data has been saved to 'output.csv'.

```

## Sample Output (Graphic)
![output screenshot Graph Traversal with Priority Nodes & Animated Visualization
](https://github.com/metaamiri/Graph-Traversal-with-Priority-Nodes-Animated-Visualization/blob/main/output%20screenshot/output.png)

## 🔧 How It Works

1. Graph Creation: create_random_graph() builds a network using networkx.

2. Traversal

   - Visits all priority nodes first using Dijkstra.

   - Visits remaining nodes in shortest possible order.

3. Visualization: animate_step_by_step() enables interactive step navigation.

4. Logging: All traversal data is written to output.csv using csv.DictWriter.

## Library Used

- networkx
- matplotlib
- csv
- random
  > install them you don't have !

## 🧠 Algorithms Used

- Dijkstra’s Algorithm: For shortest path calculation between nodes

- Greedy Heuristic: Always chooses the closest unvisited priority/regular node

- Graph Layout: spring_layout for aesthetic visualization

## Usage
Run *main.py*
