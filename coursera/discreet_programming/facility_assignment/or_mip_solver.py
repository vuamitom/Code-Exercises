from ortools.linear_solver import pywraplp

from data import Facility, Customer, Point, length

def mip_solve(facilities, customers):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    solver.SetTimeLimit(240 * 1000)
    # Create variables
    x = {}
    for i in range(len(facilities)):
        for j in range(len(customers)):
            x[i, j] = solver.IntVar(0, 1, f'x_{i}_{j}')

    # Create binary variables for facility usage
    y = {i: solver.IntVar(0, 1, f'y_{i}') for i in range(len(facilities))}

    # Constraints: Each customer must be assigned to exactly one facility
    for j in range(len(customers)):
        solver.Add(sum(x[i, j] for i in range(len(facilities))) == 1)

    # Constraints: Facility capacity must not be exceeded
    for i in range(len(facilities)):
        solver.Add(sum(x[i, j] * customers[j].demand for j in range(len(customers))) <= facilities[i].capacity)

    # Constraints: Link x and y variables
    M = sum(f.capacity for f in facilities)  # Big M constant
    for i in range(len(facilities)):
        solver.Add(sum(x[i, j] for j in range(len(customers))) <= M * y[i])

    # Objective: Minimize total cost (assignment cost + fixed cost)
    objective = solver.Objective()
    for i in range(len(facilities)):
        for j in range(len(customers)):
            objective.SetCoefficient(x[i, j], length(customers[j].location, facilities[i].location))
        objective.SetCoefficient(y[i], facilities[i].setup_cost)
    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        # Prepare the solution in the specified output format
        # if status == pywraplp.Solver.OPTIMAL:
        solution = [-1] * len(customers)
        for j in range(len(customers)):
            for i in range(len(facilities)):
                if x[i, j].solution_value() > 0:
                    solution[j] = i
                    break

        used = [0] * len(facilities)
        for i in solution:
            used[i] = 1
        # Calculate the cost of the solution    
        obj = sum([f.setup_cost * used[f.index] for f in facilities])
        for j, customer in enumerate(customers):
            obj += length(customer.location, facilities[solution[j]].location)
        return (obj, status == pywraplp.Solver.OPTIMAL, solution)
    else:
        print('No solution found within the time limit')

                

# def warehouse_assignment_single_assignment():
#     solver = pywraplp.Solver.CreateSolver('SCIP')
#     solver.SetTimeLimit(180 * 1000)
#     # Define the data
#     warehouses = ['A', 'B', 'C']
#     products = ['P1', 'P2', 'P3', 'P4']
    
#     capacities = {'A': 100, 'B': 80, 'C': 120}
#     fixed_costs = {'A': 1000, 'B': 800, 'C': 1200}
#     volumes = {'P1': 30, 'P2': 20, 'P3': 40, 'P4': 10}
    
#     costs = {
#         ('A', 'P1'): 10, ('A', 'P2'): 15, ('A', 'P3'): 20, ('A', 'P4'): 25,
#         ('B', 'P1'): 12, ('B', 'P2'): 18, ('B', 'P3'): 22, ('B', 'P4'): 20,
#         ('C', 'P1'): 15, ('C', 'P2'): 20, ('C', 'P3'): 25, ('C', 'P4'): 30
#     }

#     # Create variables
#     x = {}
#     for w in warehouses:
#         for p in products:
#             x[w, p] = solver.IntVar(0, 1, f'x_{w}_{p}')

#     # Create binary variables for warehouse usage
#     y = {w: solver.IntVar(0, 1, f'y_{w}') for w in warehouses}

#     # Constraints: Each product must be assigned to exactly one warehouse
#     for p in products:
#         solver.Add(sum(x[w, p] for w in warehouses) == 1)

#     # Constraints: Warehouse capacity must not be exceeded
#     for w in warehouses:
#         solver.Add(sum(x[w, p] * volumes[p] for p in products) <= capacities[w])

#     # Constraints: Link x and y variables
#     M = sum(capacities.values())  # Big M constant
#     for w in warehouses:
#         solver.Add(sum(x[w, p] for p in products) <= M * y[w])

#     # Objective: Minimize total cost (assignment cost + fixed cost)
#     objective = solver.Objective()
#     for w in warehouses:
#         for p in products:
#             objective.SetCoefficient(x[w, p], costs[w, p])
#         objective.SetCoefficient(y[w], fixed_costs[w])
#     objective.SetMinimization()

#     # Solve the problem
#     status = solver.Solve()

#     # Print the solution
#     if status == pywraplp.Solver.OPTIMAL:
#         print('Total cost =', solver.Objective().Value())
#         for w in warehouses:
#             if y[w].solution_value() > 0:
#                 print(f'Warehouse {w} is used:')
#                 warehouse_cost = fixed_costs[w]
#                 for p in products:
#                     if x[w, p].solution_value() > 0:
#                         print(f'  - Stores product {p}')
#                         warehouse_cost += costs[w, p]
#                 print(f'  Total cost for Warehouse {w}: {warehouse_cost}')
#             else:
#                 print(f'Warehouse {w} is not used')
        
#         print("\nProduct Assignments:")
#         for p in products:
#             for w in warehouses:
#                 if x[w, p].solution_value() > 0:
#                     print(f'Product {p} is assigned to Warehouse {w}')
#     else:
#         print('The problem does not have an optimal solution.')

# if __name__ == '__main__':
#     warehouse_assignment_single_assignment()