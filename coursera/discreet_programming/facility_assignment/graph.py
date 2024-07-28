import matplotlib.pyplot as plt
import numpy as np

def plot(facilities, customers):

    # Plot facilities
    plt.scatter([f.location.x for f in facilities], [f.location.y for f in facilities], c='r', marker='s', label='Facilities')
    # Plot customers
    plt.scatter([c.location.x for c in customers], [c.location.y for c in customers], c='b', marker='o', label='Customers')
    # Annotate facilities
    # for f in facilities:
    #     plt.annotate(f'F{f.index}', (f.location.x, f.location.y))
    # # Annotate customers
    # for c in customers:
    #     plt.annotate(f'C{c.index}', (c.location.x, c.location.y))
    # plt.legend()
    plt.show()

def plot_solutions(facilities, customers, solution):
    # Plot facilities
    plt.scatter([f.location.x for f in facilities], [f.location.y for f in facilities], c='r', marker='s', label='Facilities')
    # Plot customers
    plt.scatter([c.location.x for c in customers], [c.location.y for c in customers], c='b', marker='o', label='Customers')    
    # Plot solution with lines joining from the customer to the facility to which it is assigned
    for c, f in enumerate(solution):        
        plt.plot([customers[c].location.x, facilities[f].location.x], [customers[c].location.y, facilities[f].location.y], 'k-')
    # plt.legend()
    plt.show()