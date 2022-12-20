#import numpy as np

#Node Class
class Node(object):
    def __init__(self, level = None, path = None, bound = 0, cost = 0):
        self.level = level
        self.path = path
        self.bound = bound
        self.cost = cost  #Newly added - to avoid recalculating
        
    def __cmp__(self, other):
        return cmp(self.bound, other.bound)
    
    def __str__(self):
        return str(tuple([self.level, self.path, self.bound, self.cost]))
    
# Calculate FirstMin and SecondMin for lower bound
def firstMin(adj, i):
    min = float('inf')
    for k in range(len(adj)):
        if adj[i][k] < min and i != k:
            min = adj[i][k]
 
    return min

def secondMin(adj, i):
    first, second = float('inf'), float('inf')
    for j in range(len(adj)):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]
 
        elif(adj[i][j] <= second and
             adj[i][j] != first):
            second = adj[i][j]
 
    return second


