#!/usr/bin/python
# -*- coding: utf-8 -*-
from ortools.sat.python import cp_model
import time
 
max_run_time = 5 * 60
 
def min_coloring_nolib(edges):
    start_time = time.time()
    # Get the number of nodes in the graph
    num_nodes = max(max(edge) for edge in edges) + 1
 
    # Initialize the colors list with -1 (unassigned color)
    colors = [-1] * num_nodes
 
    # create a map of nodes to their neighbors
    neighbors = {}
    for u, v in edges:
        neighbors[u] = neighbors.get(u, []) + [v]
        neighbors[v] = neighbors.get(v, []) + [u]
 
    # Calculate the minimum degree of any node
    min_degree, max_degree = get_min_max_degree(edges)
 
    # Helper function to check if a color can be assigned to a node
    def is_safe(node, color):
        for neighbor in neighbors.get(node, []):
            if colors[neighbor] == color:
                return False
        return True
 
    min_colors_used = max_degree - 1
    result_colors = [-1] * num_nodes
    # Recursive function to perform backtracking
    def solve(node, max_color):
        nonlocal min_colors_used        
        if max_color >= min_colors_used:
            return 
        for c in range(max_color + 2):
            # if time.time() - start_time > 5 * 3600:
            #     return  
            # print(f'Node: {node}, Color: {c} isSafe {is_safe(node, c)}')
            if is_safe(node, c):
                colors[node] = c
                if node == num_nodes - 1:
                    if max_color < min_colors_used:
                        min_colors_used = min(min_colors_used, max_color)
                        result_colors[:] = colors[:]                    
                else:
                    solve(node + 1, max(max_color, c))                                      
                colors[node] = -1                                   
 
    # Start the backtracking process from node 0
    solve(0, 0)
    return min_colors_used + 1, result_colors, time.time() - start_time <= max_run_time
 
def min_coloring_nolib2(edges):
    start_time = time.time()
    # Get the number of nodes in the graph
    num_nodes = max(max(edge) for edge in edges) + 1
 
    # create a map of nodes to their neighbors
    neighbors = {}
    for u, v in edges:
        neighbors[u] = neighbors.get(u, []) + [v]
        neighbors[v] = neighbors.get(v, []) + [u]
 
    # Initialize the colors list with -1 (unassigned color)
    colors = [-1] * num_nodes    
    def force_stop():
        return time.time() - start_time > max_run_time
 
    # Calculate the minimum degree of any node
    max_degree = max(len(neighbors[node]) for node in range(num_nodes))
    nodes_by_degree = sorted(range(num_nodes), key=lambda node: len(neighbors[node]), reverse=True)
 
    choices = [[0] * max_degree for _ in range(num_nodes)]
    min_colors_used = max_degree - 1
    result_colors = [-1] * num_nodes
    # Recursive function to perform backtracking
    def mark(node, color, choices, value):
        for neighbor in neighbors[node]:
            choices[neighbor][color] += value
 
    # max_color = 0
    # for node in nodes_by_degree:
    #     for c in range(max_color + 2):
    #         if choices[node][c] == 0:
    #             colors[node] = c
    #             mark(node, c, choices, 1)
    #             max_color = max(max_color, c)
 
    def solve(nodeIdx, max_color):
        node = nodes_by_degree[nodeIdx]
        nonlocal min_colors_used        
        if max_color >= min_colors_used:
            return 
        for c in range(max_color + 2):
            if force_stop():
                return 
            if choices[node][c] == 0:
                colors[node] = c
                mark(node, c, choices, 1)
                if nodeIdx == num_nodes - 1:
                    if max_color < min_colors_used:
                        min_colors_used = min(min_colors_used, max(max_color, c))
                        result_colors[:] = colors[:]                    
                else:
                    solve(nodeIdx + 1, max(max_color, c))                                      
                colors[node] = -1 
                mark(node, c, choices, -1)                                  
 
    # Start the backtracking process from node 0
    solve(0, 0)
 
    return min_colors_used + 1, result_colors, not force_stop()
 
def min_coloring(edges):
    # Create the CP-Solver model
    model = cp_model.CpModel()
 
    # Get the number of nodes in the graph
    num_nodes = max(max(edge) for edge in edges) + 1
 
    # Calculate the minimum degree of any node
    min_degree, max_degree = get_min_max_degree(edges)
 
    # Create a variable for each node's color
    colors = [model.NewIntVarFromDomain(cp_model.Domain.FromValues(range(max_degree)), f'node{i}') for i in range(num_nodes)]
 
    # Break the symmetry of colors by ordering them
    for i in range(num_nodes):
        model.Add(colors[i] <= (i + 1))
 
    # Add constraints to ensure no two adjacent nodes have the same color
    for u, v in edges:
        model.Add(colors[u] != colors[v])
 
 
    # Add a constraint that the number of colors is greater than or equal to the minimum degree
    num_colors = model.NewIntVar(1, max_degree, 'num_colors')
    model.AddMaxEquality(num_colors, colors)        
    # model.AddDecisionStrategy(colors, cp_model.CHOOSE_FIRST, cp_model.SELECT_MIN_VALUE)    
 
    # Minimize the number of colors
    model.Minimize(num_colors)
 
    # Solve the model
    solver = cp_model.CpSolver()
    # Set the time limit for the solver
    solver.parameters.max_time_in_seconds = max_run_time
    # db = solver.Solve(model, HighDegreeDecisionBuilder(colors, edges))
    db = solver.Solve(model)
    node_colors = [solver.Value(colors[i]) for i in range(num_nodes)]
    return solver.Value(num_colors) + 1, node_colors, db ==  cp_model.OPTIMAL
 
def min_coloring2(edges):
    # Create the CP-Solver model
    model = cp_model.CpModel()
 
    # Get the number of nodes in the graph
    num_nodes = max(max(edge) for edge in edges) + 1
 
    # create a map of nodes to their neighbors
    neighbors = {}
    for u, v in edges:
        neighbors[u] = neighbors.get(u, []) + [v]
        neighbors[v] = neighbors.get(v, []) + [u]
 
    # Calculate the minimum degree of any node
    max_degree = max(len(neighbors[node]) for node in range(num_nodes))
    nodes_sorted_by_degree = sorted(range(num_nodes), key=lambda node: len(neighbors[node]), reverse=True)
    node_to_degree = {node: idx for idx, node in enumerate(nodes_sorted_by_degree)}
 
    # Create a variable for each node's color
    colors = [model.NewIntVarFromDomain(cp_model.Domain.FromValues(range(max_degree)), f'node{i}') for i in range(num_nodes)]
 
    # Break the symmetry of colors by ordering them
    for i in range(num_nodes):
        model.Add(colors[i] <= (i + 1))
 
    # Add constraints to ensure no two adjacent nodes have the same color
    for u, v in edges:
        node_u, node_v = node_to_degree[u], node_to_degree[v]
        model.Add(colors[node_u] != colors[node_v])
 
 
    # Add a constraint that the number of colors is greater than or equal to the minimum degree
    num_colors = model.NewIntVar(1, max_degree, 'num_colors')
    model.AddMaxEquality(num_colors, colors)        
    model.AddDecisionStrategy(colors, cp_model.CHOOSE_FIRST, cp_model.SELECT_MIN_VALUE)    
 
    # Minimize the number of colors
    model.Minimize(num_colors)
 
    # Solve the model
    solver = cp_model.CpSolver()
    # Set the time limit for the solver
    solver.parameters.max_time_in_seconds = max_run_time
    # db = solver.Solve(model, HighDegreeDecisionBuilder(colors, edges))
    db = solver.Solve(model)
    node_colors = [solver.Value(colors[i]) for i in range(num_nodes)]
    actual_node_colors = [-1] * num_nodes
    for idx, color in enumerate(node_colors):
        actual_node_colors[nodes_sorted_by_degree[idx]] = color
    return solver.Value(num_colors) + 1, actual_node_colors, db ==  cp_model.OPTIMAL
 
def get_min_max_degree(edges):
    degree = {}
    for u, v in edges:
        degree[u] = degree.get(u, 0) + 1
        degree[v] = degree.get(v, 0) + 1
    return min(degree.values()), max(degree.values())
 
 
def validate_solution(edges, colors):
    # Check that no two adjacent nodes have the same color
    for u, v in edges:
        if colors[u] == colors[v]:
            return False
    return True
 
def solve_it(input_data):
    # Modify this code to run your optimization algorithm
 
    # parse the input
    lines = input_data.split('\n')
 
    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
 
    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
 
    # build a trivial solution
    # every node has its own color
    # solution = range(0, node_count)
    start_time = time.time()
    # profiler = cProfile.Profile()
    # profiler.enable()                
    num_colors, colors, optimal = min_coloring2(edges)
    # profiler.disable()
    # profiler.print_stats(sort='time')
    end_time = time.time()
    execution_time = end_time - start_time
    # print(f"Execution time: {execution_time} seconds")
    # # prepare the solution in the specified output format
    # print(f'validate result : {validate_solution(edges, colors)}')
    output_data = str(num_colors) + ' ' + str(0 if not optimal else 1) + '\n'
    output_data += ' '.join(map(str, colors))
 
    return output_data
 
 
import sys
import cProfile
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')