#!/usr/bin/python
from ortools.sat.python import cp_model

# -*- coding: utf-8 -*-
def min_coloring(edges):
    # Create the CP-Solver model
    model = cp_model.CpModel()

    # Get the number of nodes in the graph
    num_nodes = max(max(edge) for edge in edges) + 1

    # Create a variable for each node's color
    colors = [model.NewIntVarFromDomain(cp_model.Domain.FromValues(range(num_nodes)), f'node{i}') for i in range(num_nodes)]

    # Add constraints to ensure no two adjacent nodes have the same color
    for u, v in edges:
        model.Add(colors[u] != colors[v])

    # Calculate the minimum degree of any node
    degrees = [0] * num_nodes
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    min_degree = min(degrees)

    # Add a constraint that the number of colors is greater than or equal to the minimum degree
    num_colors = model.NewIntVar(min_degree, num_nodes, 'num_colors')
    model.AddMaxEquality(num_colors, colors)

    # Break the symmetry of colors by ordering them
    for i in range(num_nodes - 1):
        model.Add(colors[i] <= colors[i + 1])

    # Minimize the number of colors
    model.Minimize(num_colors)

    # Solve the model
    solver = cp_model.CpSolver()
    # Set the time limit for the solver
    solver.parameters.max_time_in_seconds = 5 * 3600  # 5 hours
    status = solver.Solve(model)

    node_colors = [solver.Value(colors[i]) for i in range(num_nodes)]
    return solver.Value(num_colors), node_colors, status == cp_model.OPTIMAL    


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
    num_colors, colors, optimal = min_coloring(edges)

    # prepare the solution in the specified output format
    output_data = str(num_colors + 1) + ' ' + str(0 if not optimal else 1) + '\n'
    output_data += ' '.join(map(str, colors))

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')


