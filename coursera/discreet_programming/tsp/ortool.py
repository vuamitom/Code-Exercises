"""Simple Travelling Salesperson Problem (TSP) between cities."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math 
from pprint import pprint


def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def create_sample_data_model():
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = [
        [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
        [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
        [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
        [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
        [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
        [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
        [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
        [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
        [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
        [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
        [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
        [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
        [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
    ]
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data

# def pretty_print_2d_array(array):
#     for row in array:
#         for item in row:
#             item = round(item)
#             print(f"{item}", end=" ")
#         print()
# def compare_2d_arrays(array1, array2):
#     """compare 2d arrays and print out differences if any"""
#     for i in range(len(array1)):
#         for j in range(len(array1[0])):
#             if array1[i][j] != array2[i][j]:
#                 print(f"array1[{i}][{j}] = {array1[i][j]} != array2[{i}][{j}] = {array2[i][j]}")

def create_data_model(points): 
    data = {}    
    """Create distance matrix for points"""
    num_points = len(points)
    distance_matrix = [[0] * num_points for i in range(num_points)]
    for i in range(num_points):
        for j in range(i + 1, num_points):
            # NOTE: google ortools does not work on floating distance 
            distance_matrix[i][j] = round(length(points[i], points[j]))
            distance_matrix[j][i] = distance_matrix[i][j]    
    data["distance_matrix"] = distance_matrix    
    # compare_2d_arrays(data["distance_matrix"], distance_matrix)
    # pretty_print_2d_array(data["distance_matrix"])
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    # print(f"Objective: {solution.ObjectiveValue()} miles")
    index = routing.Start(0)
    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    route = []
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        route.append(manager.IndexToNode(previous_index))
    plan_output += f" {manager.IndexToNode(index)}\n"
    # print(plan_output)
    plan_output += f"Route distance: {route_distance}miles\n"
    return route


def solve_with_ortools(points = None):
    """Entry point of the program."""
    # Instantiate the data problem.

    data = create_sample_data_model() if points is None else create_data_model(points)
    # print('done preparing data')
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        # print('>>>>> dist ', from_node, to_node, round(data["distance_matrix"][from_node][to_node]))
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    # routing.SetTimeLimit(10000)
    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    # search_parameters.time_limit_ms = 60000
    # search_parameters.trace_propagation = True
    # search_parameters.log_search = True
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    # print('Start solving:')
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    # if solution:
    route = print_solution(manager, routing, solution)
    return route 


if __name__ == "__main__":
    solve_with_ortools()