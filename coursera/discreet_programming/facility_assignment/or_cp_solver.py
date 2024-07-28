from data import Facility, Customer, Point, length
from ortools.sat.python import cp_model

def get_bounding_box(facilities, customers):
    # get bounding box of all facilities and customers 
    ys = [f.location.y for f in facilities] + [c.location.y for c in customers]
    xs = [f.location.x for f in facilities] + [c.location.x for c in customers]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    return min_x, max_x, min_y, max_y

def cp_sat_solve(facilities, customers):
    # implement facility assignment solution using google OR CP-SAT solver
    model = cp_model.CpModel()
    # Create variables
    x = {}
    for i in range(len(facilities)):
        for j in range(len(customers)):
            x[i, j] = model.NewBoolVar(f'x_{i}_{j}')
    
    # Create binary variables for facility usage
    y = {i: model.NewBoolVar(f'y_{i}') for i in range(len(facilities))}

    # Constraints: Each product must be assigned to exactly one warehouse
    for c in range(len(customers)):
        model.Add(sum(x[w, c] for w in range(len(facilities))) == 1)

    # Constraints: Warehouse capacity must not be exceeded
    for i in range(len(facilities)):
        model.Add(sum(x[i, j] * customers[j].demand for j in range(len(customers))) <= facilities[i].capacity)
        
    # Constraints: Link x and y variables
    for w in range(len(facilities)):
        for p in range(len(customers)):
            model.Add(x[w, p] <= y[w])

    # The number of customers assigned to a warehouse must be at least 1 if the warehouse is used
    # for f in range(len(facilities)):
    #     model.Add(sum(x[f, c] for p in range(len(customers))) >= y[f])

    # Order the use of warehouses with the same characteristics
    for i in range(len(facilities)):
        for j in range(i, len(facilities)):
            if facilities[i].setup_cost == facilities[j].setup_cost and facilities[i].capacity == facilities[j].capacity and facilities[i].location == facilities[j].location:
                model.Add(y[i] >= y[j])

    # If a product's volume exceeds a warehouse's capacity, it can't be assigned there
    for f in range(len(facilities)):
        for c in range(len(customers)):
            if customers[c].demand > facilities[f].capacity:
                model.Add(x[w, p] == 0)

    if len(facilities) > 100:
        # some heuristic constraints 
        min_x, max_x, min_y, max_y = get_bounding_box(facilities, customers)
        max_x_diff = (max_x - min_x) / 6
        max_y_diff = (max_y - min_y) / 6
        # do not assign a customer to a facility if the distance between them is greater than the half of the bounding box
        for f in range(len(facilities)):
            for c in range(len(customers)):
                if abs(facilities[f].location.x - customers[c].location.x) > max_x_diff or abs(facilities[f].location.y - customers[c].location.y) > max_y_diff:
                    model.Add(x[f, c] == 0)

    # Objective: Minimize total cost (assignment cost + fixed cost)
    total_cost = sum(x[w, p] * length(facilities[w].location, customers[p].location) for w in range(len(facilities)) for p in range(len(customers))) + \
                 sum(y[w] * facilities[w].setup_cost for w in range(len(facilities)))
    model.Minimize(total_cost)
    # Create a solver and solve the model
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 360
    status = solver.Solve(model)
    # print the total run time of solver 
    # print("Time = ", solver.WallTime())
    # Print the solution
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # print('Total cost =', solver.ObjectiveValue())
        solution = [-1] * len(customers)
        obj = 0
        for w in range(len(facilities)):
            if solver.BooleanValue(y[w]):
                obj += facilities[w].setup_cost            
        
        # print("\nProduct Assignments:")
        for c in range(len(customers)):
            for f in range(len(facilities)):
                if solver.BooleanValue(x[f, c]):
                    solution[c] = f     
        # Calculate the cost of the solution
        for j, customer in enumerate(customers):
            obj += length(customer.location, facilities[solution[j]].location)        
        return (obj, status == cp_model.OPTIMAL, solution)       
    else:
        print('No solution found within the time limit')



# def cp_sat_solve_v2(facilities, customers):
 

#     data = pd.read_table(io.StringIO(data_str), sep=r"\s+")

#     # Model
#     model = cp_model.CpModel()

#     # Variables
#     x = model.new_bool_var_series(name="x", index=data.index)

#     # Constraints
#     # Each worker is assigned to at most one task.
#     for unused_name, tasks in data.groupby("worker"):
#         model.add_at_most_one(x[tasks.index])

#     # Each task is assigned to exactly one worker.
#     for unused_name, workers in data.groupby("task"):
#         model.add_exactly_one(x[workers.index])

#     # Objective
#     model.minimize(data.cost.dot(x))

#     # Solve
#     solver = cp_model.CpSolver()
#     status = solver.solve(model)

#     # Print solution.
#     if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
#         print(f"Total cost = {solver.objective_value}\n")
#         selected = data.loc[solver.boolean_values(x).loc[lambda x: x].index]
#         for unused_index, row in selected.iterrows():
#             print(f"{row.task} assigned to {row.worker} with a cost of {row.cost}")
#     elif status == cp_model.INFEASIBLE:
#         print("No solution found")
#     else:
#         print("Something is wrong, check the status and the log of the solve")
    
    