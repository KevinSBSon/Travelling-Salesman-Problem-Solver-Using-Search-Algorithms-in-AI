from queue import PriorityQueue
import math
from itertools import permutations
from bnbUtil import*

#BnB DFS Using Priority Queue
def bnb_pq(adj_matrix):
    #Initialize Variables
    opt_path = []
    n = len(adj_matrix)
    opt_cost = float('inf')
    final_path = [None] * (n + 1)
    curr = Node(level = 1, path = [-1]*(n+1))
    
    #Calculate initial bound
    for i in range(n):
        curr.bound += (firstMin(adj_matrix, i) +
                       secondMin(adj_matrix, i))
    curr.bound = math.ceil(curr.bound/2)

    curr.path[0] = 0
    pq = PriorityQueue()      #Initialize PriorityQueue
    k = 0     #k for tie breaking in PriorityQueue
    pq.put((curr.bound, k, curr)) #Put Node in PQ with bound and k
    cnt = 0   #Initialize Node Count
    
    
    while not pq.empty():   #Do iteration during PQ has a node in it
        curr = pq.get()[2]  #Pick a node from PQ
        level = curr.level
        visited = [False] * n  #Set visited list
        for j in range(level):
            if curr.path[j] != -1:
                visited[curr.path[j]] = True
        
        #When node contaion a full path, it checks its cost
        if level == n:
            #cnt += 1  #Counting an explored leaf node
            if adj_matrix[curr.path[level - 1]][curr.path[0]] != 0:
                res_cost = curr.cost + adj_matrix[curr.path[level - 1]][curr.path[0]]
                if res_cost < opt_cost:
                    final_path[:n + 1] = curr.path[:]
                    final_path[n] = curr.path[0]
                    opt_cost = res_cost
                    continue
        
        for i in range(n):
            k += 1
            if (adj_matrix[curr.path[level-1]][i] != 0 and visited[i] == False):
                temp = curr
                curr = Node(level = curr.level, path = curr.path[:], bound = curr.bound, cost = curr.cost)
                curr.cost += adj_matrix[curr.path[level - 1]][i]
            
                if level == 1:
                    curr.bound -= ((firstMin(adj_matrix, curr.path[level - 1]) + firstMin(adj_matrix, i)) / 2)
                    
                else:
                    curr.bound -= ((secondMin(adj_matrix, curr.path[level - 1]) + firstMin(adj_matrix, i)) / 2)
                
                if curr.bound + curr.cost < opt_cost:# + 0.5*opt_cost: #Multiplying 0.5 is added for dealing with the map is generated with a low standard deviation
                    cnt += 1  #Counting # of expanded node
                    curr.path[level] = i
                    visited[i] = True
                    curr.level += 1
                    pq.put((curr.bound + curr.cost, k, curr))
                else:
                    del curr
                curr = temp
    return final_path, opt_cost, cnt
