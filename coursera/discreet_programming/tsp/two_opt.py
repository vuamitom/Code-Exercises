import math 

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def create_distance_matrix(points):     
    """Create distance matrix for points"""    
    num_points = len(points)
    distance_matrix = [[0] * num_points for i in range(num_points)]
    for i in range(num_points):
        for j in range(i + 1, num_points):
            # NOTE: google ortools does not work on floating distance 
            distance_matrix[i][j] = round(length(points[i], points[j]))
            distance_matrix[j][i] = distance_matrix[i][j]    
    return distance_matrix

def two_opt_b(tour, distMat):
    
    # distMat = create_distance_matrix(points)
    
    ncities = len(tour)
    
    # print(f"{compute_length(tour)} ", end="")
    
    improvement_flag = True
    num_exchanges = 0
    
    while improvement_flag:
        improvement_flag = False
        max_gain = 0
        
        for i in range(ncities - 2):
            n_inner_loop = ncities if i else ncities - 1
            
            for j in range(i + 2, n_inner_loop):
                remove = distMat[tour[i]][tour[i+1]] + distMat[tour[j]][tour[(j+1) % ncities]]
                add = distMat[tour[i]][tour[j]] + distMat[tour[i+1]][tour[(j+1) % ncities]]
                
                gain = -remove + add
                if gain < max_gain:
                    improvement_flag = True
                    max_gain = gain
                    h, l = i + 1, j
        
        if improvement_flag:
            num_exchanges += 1
            tour[h:l+1] = reversed(tour[h:l+1])
    
    # Uncomment the following line if you want to print the final results
    # print(f"{compute_length(tour)} {num_exchanges} {num_exchanges+1} {abs(elapsed_time(VIRTUAL))}")
    
    return tour
