import matplotlib
matplotlib.use('TkAgg')  # Ensure the backend supports interactive widgets

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random
import csv

# initializing graph
def create_random_graph(num_nodes, min_edges_per_node, max_edges_per_node):
    G = nx.Graph()

    for i in range(num_nodes):
        G.add_node(i)

    for node in range(num_nodes):
        while len(list(G.neighbors(node))) < min_edges_per_node:
            target = random.choice(range(num_nodes))
            if (target != node) and (not G.has_edge(node, target)) and (len(list(G.neighbors(target))) < max_edges_per_node):
                weight = random.randint(1, 20)
                G.add_edge(node, target, weight=weight)

    return G

# function to create frame and animation
def animate_step_by_step(G, pos, full_path, priority_nodes):
    fig, ax = plt.subplots(figsize=(7, 7))

    step = [0]  # track the current step

    def update():
        ax.clear()

        # Draw all nodes and edges
        nx.draw(G, pos, with_labels=True, ax=ax, node_color="skyblue", node_size=500, font_size=10, font_weight="bold")

        # Highlight priority nodes
        nx.draw_networkx_nodes(G, pos, nodelist=priority_nodes, node_color="red", node_size=500, ax=ax)

        # Highlight visited part of the path
        if step[0] > 0:
            nx.draw_networkx_edges(G, pos, edgelist=full_path[:step[0]], edge_color="orange", width=2, ax=ax)

        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)

        ax.set_title(f"Step {step[0]} of {len(full_path)}")
        plt.draw()

    def next_step(event):
        if step[0] < len(full_path):
            step[0] += 1
            update()

    def prev_step(event):
        if step[0] > 0:
            step[0] -= 1
            update()

    update()

    # Add buttons for controlling the animation
    ax_next = plt.axes([0.8, 0.01, 0.1, 0.075])
    ax_prev = plt.axes([0.7, 0.01, 0.1, 0.075])
    btn_next = Button(ax_next, 'Next')
    btn_prev = Button(ax_prev, 'Prev')

    btn_next.on_clicked(next_step)
    btn_prev.on_clicked(prev_step)

    plt.show()

def find_combined_shortest_path_with_buttons(G, start_node, priority_nodes, num_nodes):
    pos = nx.spring_layout(G)
    visited_priority_nodes = []
    current_node = start_node
    total_distance = 0
    total_time = 0
    full_path = []
    file_name = "output.csv"

    step = 0
    while priority_nodes:
        shortest_path = None
        shortest_distance = float('inf')
        next_priority_node = None

        # Finding node with the shortest path
        for target in priority_nodes:
            path_length = nx.dijkstra_path_length(G, source=current_node, target=target, weight='weight')
            if path_length < shortest_distance:
                shortest_distance = path_length
                shortest_path = nx.dijkstra_path(G, source=current_node, target=target, weight='weight')
                next_priority_node = target

        if shortest_path is not None:
            step += 1
            total_time += 0.5
            road_time = shortest_distance / 60
            print(f"Shortest path from node {current_node} to priority node {next_priority_node}: {shortest_path} "
                  f"with shortest distance {shortest_distance} , visit time unil now : {total_time} and with road time : {round(road_time, 1)}")

            # Save data in csv file
            save_to_csv(file_name, {
                "Step": step,
                "Source": current_node,
                "Target": next_priority_node,
                "Path": shortest_path,
                "Distance": shortest_distance,
                "Visit Time (hours)": total_time,
                "Road Time (hours)": round(road_time, 1),
                "Average Time Per Node": "-"
            })
            total_distance += shortest_distance
            full_path.extend([(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)])
            visited_priority_nodes.append(next_priority_node)
            priority_nodes.remove(next_priority_node)
            current_node = next_priority_node

    visited_nodes = set(visited_priority_nodes)
    remaining_nodes = set(G.nodes()) - visited_nodes

    while remaining_nodes:
        shortest_path = None
        shortest_distance = float('inf')
        next_node = None

        for target in remaining_nodes:
            path_length = nx.dijkstra_path_length(G, source=current_node, target=target, weight='weight')
            if path_length < shortest_distance:
                shortest_distance = path_length
                shortest_path = nx.dijkstra_path(G, source=current_node, target=target, weight='weight')
                next_node = target

        if shortest_path is not None:
            step += 1
            total_time += 0.5
            road_time = shortest_distance / 60
            print(f"Shortest path from node {current_node} to node {next_node}: {shortest_path} "
                  f"with shortest distance {shortest_distance} , visit time unil now : {total_time} and with road time : {round(road_time, 1)}")
            save_to_csv(file_name, {
                "Step": step,
                "Source": current_node,
                "Target": next_node,
                "Path": shortest_path,
                "Distance": shortest_distance,
                "Visit Time (hours)": total_time,
                "Road Time (hours)": round(road_time, 1),
                "Average Time Per Node": "-"
            })
            total_distance += shortest_distance
            full_path.extend([(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)])
            visited_nodes.update(shortest_path[:]) # نود های در مسیر
            # visited_nodes.add(next_node)
            remaining_nodes.remove(next_node)  # next node is visited
            current_node = next_node

    total_road_time = round(total_distance / 60, 1)
    avg_time_per_node = round((total_road_time + total_time) / num_nodes, 2)
    print(f"Total distance to visit all nodes: {total_distance}")
    print(f"Time spent visiting all nodes: {total_time} hours")
    print(f"Time on road : {total_road_time} hours")
    print(f"Total time spent visiting and riding : {total_road_time + total_time} hours")
    print(f"Average time to fill each atm : {avg_time_per_node}")

    save_to_csv(file_name, {
        "Step": "Summary",
        "Source": "-",
        "Target": "-",
        "Path": "All",
        "Distance": total_distance,
        "Visit Time (hours)": total_time,
        "Road Time (hours)": total_road_time,
        "Average Time Per Node": avg_time_per_node
    })

    print(f"Data has been saved to '{file_name}'.")

    animate_step_by_step(G, pos, full_path, visited_priority_nodes)
    return visited_priority_nodes, visited_nodes, total_distance, total_time

# Function to save data to CSV
def save_to_csv(file_name, data, is_header=False):
    with open(file_name, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if is_header:
            writer.writeheader()  # Write header if it's the first row
            return
        writer.writerow(data)

# Initialize the CSV file with headers
file_name = "output.csv"
save_to_csv(file_name, {
    "Step": "Step",
    "Source": "Source",
    "Target": "Target",
    "Path": "Path",
    "Distance": "Distance",
    "Visit Time (hours)": "Visit Time (hours)",
    "Road Time (hours)": "Road Time (hours)",
    "Average Time Per Node": "Average Time Per Node"
}, is_header=True)

# Parameters
num_nodes = random.randint(5, 10)
min_edges_per_node = 2
max_edges_per_node = 4
priority_nodes = random.sample(range(num_nodes),random.randint(2, 4) )

random_graph = create_random_graph(num_nodes, min_edges_per_node, max_edges_per_node)
start_node = random.choice(range(num_nodes))

print("Priority nodes:", priority_nodes)
print("Start node:", start_node)

priority_nodes_copy = priority_nodes.copy()
find_combined_shortest_path_with_buttons(random_graph, start_node, priority_nodes_copy, num_nodes)
