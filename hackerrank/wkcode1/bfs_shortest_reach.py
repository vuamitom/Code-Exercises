#!/bin/python3

import math
import os
import random
import re
import sys
import heapq 


#
# Complete the 'bfs' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER m
#  3. 2D_INTEGER_ARRAY edges
#  4. INTEGER s
#

def bfs(n, m, edges, s):
    # Write your code here
    graph = [None] * n 
    for edge in edges: 
        start, end = edge         
        graph[start-1] = graph[start-1] if graph[start-1] is not None else [] 
        graph[end-1] = graph[end-1] if graph[end-1] is not None else [] 
        graph[start-1].append(end)
        graph[end-1].append(start)
    check=[]
    min_dist = [-1] * n 
    # print('graph=',graph)
    heapq.heappush(check, (0, s))
    while len(check) > 0:
        dist, node = heapq.heappop(check)
        # print('dist, node ', dist, node)
        if min_dist[node - 1] == -1 or min_dist[node - 1] > dist:
            min_dist[node - 1] = dist 
        else:
            continue 
        cur_dist = min_dist[node - 1]
        if graph[node-1] is not None:
            for e in graph[node - 1]:
                if cur_dist + 6 < min_dist[e - 1] or min_dist[e-1] == -1:
                    heapq.heappush(check, (cur_dist + 6, e))
    return [val for idx, val in enumerate(min_dist) if not idx + 1 == s]

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input().strip())

    for q_itr in range(q):
        first_multiple_input = input().rstrip().split()

        n = int(first_multiple_input[0])

        m = int(first_multiple_input[1])

        edges = []

        for _ in range(m):
            edges.append(list(map(int, input().rstrip().split())))

        s = int(input().strip())

        result = bfs(n, m, edges, s)

        fptr.write(' '.join(map(str, result)))
        fptr.write('\n')

    fptr.close()
