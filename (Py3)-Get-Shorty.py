"""
https://open.kattis.com/problems/getshorty/
A program to find the greatest route through a graph of multiplicative costs between 0 and 1.
"""


from queue import PriorityQueue
from collections import defaultdict


# edge_dict connects vertex keys to list values. If vertex A is in the list value of the vertex B key, it means that
# A and B are connected
# cost_dict connects tuples of two vertexes (the keys) with int values.
# If cost_dict[(A, B)] = 4, then B is connected to A at a cost/distance of 4
class Graph:
    def __init__(self):
        self.vertex_set = set()
        self.edge_dict = defaultdict(list)
        self.cost_dict = {}

    def add_vertex(self, value):
        self.vertex_set.add(value)

    def add_edge(self, source, target, cost):
        self.edge_dict[source].append(target)
        self.edge_dict[target].append(source)
        self.cost_dict[(source, target)] = cost
        self.cost_dict[(target, source)] = cost


# This modified algorithm finds the route from the source to the target with the maximal cost, instead of minimal
def modified_dijkstra_algorithm(graph, source, target):
    # Initialize the source to be at cost 1 from itself
    cost_from_source = {source: 1}
    vertexes_priority_queue = PriorityQueue()

    # Initialize every vertex in our graph to have a base cost to reach from the source of 0
    # (except for the source itself)
    for vertex in graph.vertex_set:
        if vertex != source:
            cost_from_source[vertex] = 0
        # Put every graph into our priority queue with a priority of its negative cost
        # This will always resolve the largest cost first
        vertexes_priority_queue.put((-cost_from_source[vertex], vertex))

    while vertexes_priority_queue:
        # Take the unexplored path connected to the source that maximizes the cost
        current_vertex = vertexes_priority_queue.get()[1]
        # If the maximal unexplored path leads to the target vertex, then we are done
        if current_vertex == target:
            return cost_from_source[current_vertex]

        # Otherwise, look at all of the neighbors of the current vertex
        for neighbor in graph.edge_dict[current_vertex]:
            # Check if a path  <source -> current_vertex -> neighbor>  has a higher cost than any path we've
            # previously found to the neighboring vertex
            alternate_path_length = cost_from_source[current_vertex] * graph.cost_dict[(neighbor, current_vertex)]

            # If so, update the value of the maximum cost from the source to that neighboring vertex
            if alternate_path_length > cost_from_source[neighbor]:
                cost_from_source[neighbor] = alternate_path_length
                vertexes_priority_queue.put((-alternate_path_length, neighbor))

    return cost_from_source[target]


while True:
    corridors_and_intersections = input()
    corridors_and_intersections_list = corridors_and_intersections.split(' ')
    corridors_total = int(corridors_and_intersections_list[0])
    intersections_total = int(corridors_and_intersections_list[1])

    # If the input is '0 0', end the program
    if corridors_total == intersections_total == 0:
        break

    new_graph = Graph()
    for corridor in range(corridors_total):
        new_graph.add_vertex(corridor)

    for intersection in range(intersections_total):
        intersection_edge = input().split(' ')
        # For each intersection, add an edge between the two vertexes we're given, with a cost as given
        new_graph.add_edge(int(intersection_edge[0]), int(intersection_edge[1]), float(intersection_edge[2]))

    # Print the solution as a string with exactly four decimals
    print(str.format('{:05.4f}', modified_dijkstra_algorithm(new_graph, 0, corridors_total - 1)))
