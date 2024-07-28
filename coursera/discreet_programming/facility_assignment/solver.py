#!/usr/bin/python
# -*- coding: utf-8 -*-
from data import Facility, Customer, Point, length
from naiive_solver import naiive_solve
from or_mip_solver import mip_solve
from or_cp_solver import cp_sat_solve
from graph import plot, plot_solutions

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3]))))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    # plot(facilities, customers)
    # return 
    # obj, is_optimal, solution = naiive_solve(facilities, customers)
    res =  cp_sat_solve(facilities, customers)
    if res is not None:
        obj, is_optimal, solution = res 
        # plot_solutions(facilities, customers, solution)
        # prepare the solution in the specified output format
        output_data = '%.2f' % obj + ' ' + str(1 if is_optimal else 0) + '\n'
        output_data += ' '.join(map(str, solution))

        return output_data
    else:
        res = mip_solve(facilities, customers)
        if res is not None:
            obj, is_optimal, solution = res 

            # prepare the solution in the specified output format
            output_data = '%.2f' % obj + ' ' + str(1 if is_optimal else 0) + '\n'
            output_data += ' '.join(map(str, solution))
            return output_data
        else:
            obj, _, solution = naiive_solve(facilities, customers)
            output_data = '%.2f' % obj + ' ' + str(0) + '\n'
            output_data += ' '.join(map(str, solution))
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

