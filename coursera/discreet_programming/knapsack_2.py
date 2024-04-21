#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    if item_count <= 50:
        value, taken = dynamic_programming(items, capacity)
    else:
        value, taken = greedy(items, capacity)
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


def trivial(items, capacity):
    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return value, taken

def greedy(items, capacity):
    # a greedy algorithm for filling the knapsack
    # it takes items with the highest value/weight ratio until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    items = sorted(items, key=lambda x: x.value/x.weight, reverse=True)
    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return value, taken

def dynamic_programming(items, capacity):
    # a dynamic programming algorithm for filling the knapsack
    # it takes items with the highest value/weight ratio until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    n = len(items)
    dp = [[0 for _ in range(capacity+1)] for _ in range(n+1)]

    for i in range(1, n+1):
        for w in range(1, capacity+1):
            if items[i-1].weight <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-items[i-1].weight] + items[i-1].value)
            else:
                dp[i][w] = dp[i-1][w]

    value = dp[n][capacity]
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            taken[i-1] = 1
            w -= items[i-1].weight

    return value, taken


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

