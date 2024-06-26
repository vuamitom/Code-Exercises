#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import random
from ortool import solve_with_ortools
import matplotlib.pyplot as plt
import numpy as np
import itertools
from two_opt import two_opt_b, create_distance_matrix

MAX_ITERATIONS = 1000
Point = namedtuple("Point", ['x', 'y'])

def is_valid_route(route):
    """
    check if the given route is valid (i.e. it visits all nodes of the graph once)
    """
    return len(route) == len(set(route))

# can try to use this later to speed up the search
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html 
def generate_initial_route(points):
    """
    Generates a initial route by greedy approach, choose shortest edge first 
    """
    # Start from the first node
    route = [0]
    current_node = 0
    unvisited_nodes = set(range(1, len(points)))
    while unvisited_nodes:
        next_node = min(unvisited_nodes, key=lambda x: length(points[current_node], points[x]))
        route.append(next_node)
        unvisited_nodes.remove(next_node)
        current_node = next_node
    return route

def get_random_initial_route(points):
    """
    Generates a initial route by randomly selecting nodes
    """
    # Start from the first node
    route = [0]
    current_node = 0
    next_node = random.choice(list(range(1, len(points))))
    route.append(next_node)
    current_node = next_node
    unvisited_nodes = set(range(1, len(points)))
    unvisited_nodes.remove(next_node)
    while unvisited_nodes:
        next_node = min(unvisited_nodes, key=lambda x: length(points[current_node], points[x]))
        route.append(next_node)
        unvisited_nodes.remove(next_node)
        current_node = next_node
    return route

def get_neighbors(route):
    """
    Generates all neighboring routes by swapping two nodes in the given route. 
    """
    neighbors = []
    for i in range(1, len(route)):
        for j in range(i + 1, len(route)):
            neighbor = route[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def get_neighbors_3opts(route):
    """
    Generates all neighboring routes by swapping two nodes in the given route. 
    """
    neighbors = []
    for i in range(1, len(route)):
        for j in range(i + 1, len(route)):
            for z in range(j + 1, len(route)):
                # get permutation of i, j, z


                neighbor = route[:]
                neighbor[i], neighbor[j], neighbor[z] = neighbor[j], neighbor[z], neighbor[i]
                neighbors.append(neighbor)            
    return neighbors

def travel_distance(solution, points):
    """
    Given a route, and coordinate of each points, calculate the total distance traveled.
    """
    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, len(points)-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj

def actual_travel_distance(solution, points):
    """
    Given a route, and coordinate of each points, calculate the total distance traveled.
    """
    # calculate the length of the tour
    obj = actual_length(points[solution[-1]], points[solution[0]])
    for index in range(0, len(points)-1):
        obj += actual_length(points[solution[index]], points[solution[index+1]])
    return obj

def length(point1, point2):
    return (point1.x - point2.x)**2 + (point1.y - point2.y)**2

def actual_length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_tsp(points, max_iterations=MAX_ITERATIONS, max_restarts=10):
    """
    Solves the TSP problem using a tabu search algorithm.
    """
    # Initialize the route
    # best_route = generate_initial_route(len(points))    
    # best_distance = travel_distance(best_route, points)
    # tabu_list = []    
    for restart in range(max_restarts):
        best_route = generate_initial_route(points)
        best_distance = travel_distance(best_route, points)
        current_route = best_route[:]             
        for i in range(max_iterations):
            if max_iterations == 1:
                break    
            # Get the neighbors of the current route            
            neighbors = get_neighbors(current_route)            
            # Find the best neighbor
            best_neighbor = None
            best_neighbor_distance = float('inf')
            for neighbor in neighbors:
                # if neighbor not in tabu_list or True:
                distance = travel_distance(neighbor, points)
                if distance < best_neighbor_distance:
                    best_neighbor = neighbor
                    best_neighbor_distance = distance            
            # Update the current route
            current_route = best_neighbor
            # print('4')
            # Update the best route
            if best_neighbor_distance < best_distance:
                best_route = best_neighbor
                best_distance = best_neighbor_distance
            else:
                break
        print ('iterations ', i + 1, 'best distance', best_distance)
        # Add the current route to the tabu list
        # tabu_list.append(current_route)
        
        # Remove the oldest route from the tabu list
        # if len(tabu_list) > tabu_tenure:
        #     tabu_list.pop(0)    
    return best_route, i + 1

# Function to generate a new solution by swapping two cities
# def swap_cities(tour):
#     new_tour = tour[:]  # Create a copy of the tour
#     i, j = random.sample(range(1, len(tour)), 2)  # Select two random cities to swap
#     new_tour[i], new_tour[j] = new_tour[j], new_tour[i]  # Swap the cities
#     return new_tour

def swap_cities(tour):
    new_tour = tour[:]  # Create a copy of the tour
    i, j = sorted(random.sample(range(1, len(tour)), 2))  # Select two random cities to swap
    # new_tour[i], new_tour[j] = new_tour[j], new_tour[i]  # Swap the cities
    if j - i == 1:
        if j < len(tour) - 1:
            j = j + 1
        else: 
            i = i - 1
    h, l = i + 1, j
    new_tour[h:l+1] = reversed(new_tour[h:l+1])
    return new_tour

def swap_cities_kopt(tour, points, k=2):
    neighbors = get_neighbors(tour) if k == 2 else get_neighbors_3opts(tour)
    best_neighbor = None
    best_neighbor_distance = float('inf')
    for neighbor in neighbors:
        # if neighbor not in tabu_list or True:
        distance = travel_distance(neighbor, points)
        if distance < best_neighbor_distance:
            best_neighbor = neighbor
            best_neighbor_distance = distance
    return best_neighbor

def swap_cities_1opt_longest_edge(tour, points):
    """
    Generates a new solution by swapping the longest edge in the tour
    """
    # Find the longest edge
    longest_edge = None
    longest_edge_length = 0
    for i in range(len(tour) - 1):
        edge_length = length(points[tour[i]], points[tour[i + 1]])
        if edge_length > longest_edge_length:
            longest_edge = (i, i + 1)
            longest_edge_length = edge_length
    edge_length = length(points[tour[-1]], points[tour[0]])
    if edge_length > longest_edge_length:
        longest_edge = (len(tour) - 1, 0)
        longest_edge_length = edge_length
    # Swap the cities in the longest edge
    new_tour = tour[:]
    i, j = longest_edge
    while i < j:
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        i += 1
        j -= 1
    return new_tour

def swap_cities_2opt_longest_edge(tour, points):
    """
    Generates a new solution by getting 2 longest edges in the tour
    and swap them 
    """
    # select the 2 longest edges 
    edges = []
    for i in range(len(tour) - 1):
        edge_length = length(points[tour[i]], points[tour[i + 1]])
        edges.append((i, i + 1, edge_length))
    edge_length = length(points[tour[-1]], points[tour[0]])
    edges.append((len(tour) - 1, 0, edge_length))
    sorted_edges = sorted(edges[:], key=lambda x: x[2], reverse=True)
    # tour = tour[:]
    i, j, k, l = sorted_edges[0][0], sorted_edges[0][1], sorted_edges[1][0], sorted_edges[1][1]
    x1, x2, y1, y2  = (i, j, k, l) if i < k else (k, l, i, j)    
    if tour[x2] == tour[y1]:
        tour = tour[:x1+1] + [tour[y2], tour[y1]] + tour[y2+1:]
    else:
        tour = tour[:x1+1] + list(reversed(tour[x2:y1+1])) + (tour[y2:] if y2 > 0 else [])    
    # print('new ', tour)
    return tour


def swap_cities_2opt_random(tour, points):
    """pick an edge randomly, and then swap ith with the longest edge"""
     # Find the longest edge
    longest_edge = None
    longest_edge_length = 0
    for i in range(len(tour) - 1):
        edge_length = length(points[tour[i]], points[tour[i + 1]])
        if edge_length > longest_edge_length:
            longest_edge = (i, i + 1)
            longest_edge_length = edge_length
    edge_length = length(points[tour[-1]], points[tour[0]])
    if edge_length > longest_edge_length:
        longest_edge = (len(tour) - 1, 0)
        longest_edge_length = edge_length
    # Swap the cities in the longest edge
    new_tour = tour[:]
    # pick a random number from 0 to len(tour) - 1
    start_point = None 
    while start_point is None or start_point in (longest_edge[0], longest_edge[1]):
        start_point = random.randint(0, len(tour) - 1)
    other_edges = start_point, (start_point + 1) % len(tour)
    i, j, k, l = longest_edge[0], longest_edge[1], other_edges[0], other_edges[1]
    x1, x2, y1, y2  = (i, j, k, l) if i < k else (k, l, i, j)
    # print('x1, x2, y1, y2', x1, x2, y1, y2, tour[x1], tour[x2], tour[y1], tour[y2])
    # print('old ', tour)
    old_tour = tour
    if tour[x2] == tour[y1]:
        if not tour[y2] == 0:
            tour = tour[:x1+1] + [tour[y2], tour[y1]] + tour[y2+1:]
        else:
            # tour = tour[:x1+1] + [tour[y2], tour[y1]] + tour[y2+1:]
            tour = tour[:]
            tour[x1], tour[x2] = tour[x2], tour[x1]
    else:
        tour = tour[:x1+1] + list(reversed(tour[x2:y1+1])) + (tour[y2:] if y2 > 0 else [])    
    # print('new ', tour)
    if not len(tour) == len(old_tour):
        print('x1, x2, y1, y2', x1, x2, y1, y2, old_tour[x1], old_tour[x2], old_tour[y1], old_tour[y2])
        print('len ', len(tour), len(old_tour))
        print('old ', old_tour)
        print('new ', tour)
        raise KeyError('length not equal')
    return tour

def traveling_salesman_hamiltonian(points):
    num_cities = len(points)
    vertices = list(range(num_cities))
    
    # Generate all permutations of the vertices (excluding the starting point)
    min_cost = float('inf')
    best_permutation = None
    
    for permutation in itertools.permutations(vertices[1:]):
        # Include the starting point (vertex 0) at the beginning and end of the permutation
        current_permutation = [0] + list(permutation)
        current_cost = travel_distance(current_permutation, points)
        
        if current_cost < min_cost:
            min_cost = current_cost
            best_permutation = current_permutation
    
    return best_permutation, min_cost


# Simulated Annealing with Metropolis heuristic
def simulated_annealing(points, max_resets=1):
    # Initialize temperature and cooling schedule
    initial_route = generate_initial_route(points)
    distMatrix = create_distance_matrix(points)
    initial_route = two_opt_b(initial_route, distMatrix)
    current_tour = None
    for turn in range(0, max_resets):
        # print('turn ', turn)
        temperature = 51
        cooling_rate = 0.9998 #if turn < 80 else (0.9 if turn < 90 else 0.8)
        # Initialize a random tour
        current_tour =  two_opt_b(initial_route, distMatrix) # if current_tour is None else get_random_initial_route(points)
        # print('initial tour', current_tour)
        best_tour = current_tour[:]
        best_distance = travel_distance(best_tour, points)
        iter = 0
        while temperature > 1:
            iter += 1
            # Generate a new tour by swapping two cities            
            new_tour = swap_cities(current_tour) # if turn > 1 else swap_cities_2opt_random(current_tour, points)
            # Calculate the difference in distances
            current_distance = travel_distance(current_tour, points)
            
            new_distance = travel_distance(new_tour, points)
            # print('current distance', current_distance, 'new_distance', travel_distance(new_tour, points))
            delta_distance = new_distance - current_distance
            # if delta_distance == 0:
            #     print('new tour', new_tour, 'current tour', current_tour, ' swap ', h, l)

            # Apply the Metropolis heuristic
            if delta_distance < 0:            
                # print('iter ', iter, ' update cur tour')     
                current_tour = new_tour
            else:                
                acceptance_probability = math.exp(-delta_distance / temperature ) * ((turn / 50) + 1)
                if random.random() < acceptance_probability:
                    # print('accept new_tour with probability', acceptance_probability, 'delta_distance', delta_distance, 'temperature', temperature)
                    # print('cur', current_tour)
                    # print('new', new_tour)
                    # visualize(points, current_tour, new_tour )
                    current_tour = new_tour

            # Update the best tour if a better solution is found
            # print('y', best_distance)
            if travel_distance(current_tour, points) < best_distance:            
                # print('iter ', iter, 'turn', turn, ' update best tour', delta_distance)
                # visualize(points, current_tour, best_tour)
                best_tour = current_tour[:]
                best_distance = travel_distance(best_tour, points)
                initial_route = best_tour                

            # Cool the temperature
            temperature *= cooling_rate
    # print('current tour', current_tour)
    best_tour = two_opt_b(best_tour, distMatrix)
    return best_tour, best_distance

def visualize(points, route, previous_route = None):
    """scatter plot the list of points. highlight edges that are not in previous route"""
    plt.figure(figsize=(10, 10))
    x = [point.x for point in points]
    y = [point.y for point in points]
    plt.scatter(x, y)
    for i in range(len(route) - 1):
        plt.plot([points[route[i]].x, points[route[i + 1]].x], [points[route[i]].y, points[route[i + 1]].y], 'ro-')
    plt.plot([points[route[-1]].x, points[route[0]].x], [points[route[-1]].y, points[route[0]].y], 'ro-')
    if previous_route:
        for i in range(len(route) - 1):
            if route[i] != previous_route[i] or route[i+1] != previous_route[i+1]:
                plt.plot([points[route[i]].x, points[route[i + 1]].x], [points[route[i]].y, points[route[i + 1]].y], 'bo-')
        if route[-1] != previous_route[-1] or route[0] != previous_route[0]:
            plt.plot([points[route[-1]].x, points[route[0]].x], [points[route[-1]].y, points[route[0]].y], 'bo-')
    plt.show()
    
    



def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    use_ortools = True
    if len(points) <= 51:        
        solution, _ = simulated_annealing(points, 200)
        # solution, _ = traveling_salesman_hamiltonian(points)        
        is_optimal = 1
    elif len(points) >= 30000:        
        solution, iterations = solve_tsp(points, 1, 1)        
        is_optimal = 0 if iterations >= MAX_ITERATIONS else 1
        # print('no of iterations:', iterations, " no restarts: ", restarts)        
    else:
        # solution, is_optimal = solve_tsp_with_ortools(points)        
        # print('Solving with ortools ', len(points))
        solution = solve_with_ortools(points)
        is_optimal = 1
    obj = actual_travel_distance(solution, points)
    output_data = '%.2f' % obj + ' ' + str(is_optimal) + '\n'
    output_data += ' '.join(map(str, solution))
    # visualize(points, solution)
    return output_data

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

