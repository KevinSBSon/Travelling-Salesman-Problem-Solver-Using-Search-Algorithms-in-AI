import numpy
import time
import os
import sys
from generate_travelling_salesman_problem import write_distance_matrix

def openFile(filename):
    f = open(filename)
    input = f.read()
    node_count=0
    distances=[]
    for idx,line in enumerate(input.splitlines()):
        if(idx==0):
            node_count=int(line)
        else:
            distances.append([float(x) for x in line.split()])
    return (node_count,distances)

def calculate_cost(path,distances):
    first=-1
    prev=-1
    distance=0
    for v in path:
        if prev==-1:
            first=v
            prev=v
            continue
        distance+=distances[prev][v]
        prev=v
    return distance+distances[prev][first]

def nearestNeighbor(distances,tabu_list=[]):
    path=[]
    prev=0
    path.append(0)
    while len(path)<len(distances):
        node=distances[prev]
        min_idx=-1
        min_dist=-1.0
        for idx, dist in enumerate(node):
            if dist==0.0:
                continue
            if idx in path:
                continue
            min_idx=idx
            min_dist=dist
            break

        for idx, dist in enumerate(node):
            if dist==0.0:
                continue
            if idx in path:
                continue
            if (prev,idx) in tabu_list:
                continue
            if min_dist > dist:
                min_idx=idx
                min_dist=dist
        path.append(min_idx)
        prev=min_idx
    return path

def two_opt(distances,path):
    best=path
    lowest_cost=calculate_cost(path,distances)
    improved=True
    while improved:
        improved=False
        for i in range(1,len(path)-1):
            for j in range(i+1,len(path)):
                if j-i==1:
                    continue
                cost_difference = -distances[path[i-1]][path[i]]-distances[path[j-1]][path[j]]+distances[path[i-1]][path[j-1]]+distances[path[i]][path[j]]
                if cost_difference < 0:
                    neighbor = path[:]
                    neighbor[i:j] = path[j-1:i-1:-1]
                    improved=True
                    best=neighbor[:]
                    path=neighbor
    return best

def keep_index_in_path(index,path_length):
    return (index+path_length)%path_length

def cost_delta_node_swap(distances,path,i,j):
    path_length=len(path)
    iprev=keep_index_in_path(i-1,path_length)
    inext=keep_index_in_path(i+1,path_length)
    jprev=keep_index_in_path(j-1,path_length)
    jnext=keep_index_in_path(j+1,path_length)
    delta=\
        distances[path[jprev]][path[i]]+\
        distances[path[jnext]][path[i]]+\
        distances[path[iprev]][path[j]]+\
        distances[path[inext]][path[j]]-\
        distances[path[iprev]][path[i]]-\
        distances[path[inext]][path[i]]-\
        distances[path[jprev]][path[j]]-\
        distances[path[jnext]][path[j]]
    #if indices are adjacent add back two subtracted edge lengths
    if iprev==j or inext==j:
        delta += 2 * distances[path[i]][path[j]]
    return delta



def simulated_annealing(distances,path):
    temperature=100.0*calculate_cost(path,distances)/len(path)
    #temp_coeff=3
    
    temp_coeff=float(len(distances))/5
    if temp_coeff>5:
        temp_coeff=5
    temp_coeff=1.0-numpy.float_power(0.1,temp_coeff)
    tabu_edges=[]
    max_tabu_edges=2+(len(distances)*(len(distances)-1))/20
    if max_tabu_edges>1000:
        max_tabu_edges=1000
    while temperature>0.000001:
        i=numpy.random.randint(0,len(path))
        j=numpy.random.randint(0,len(path))
        if i==j or (i,j) in tabu_edges or (j,i) in tabu_edges:
            continue
        cost = cost_delta_node_swap(distances,path,i,j)
        if cost<0 or numpy.random.random() < numpy.exp(-cost/temperature):
            tabu_edges.append((i,j))
            if len(tabu_edges)>max_tabu_edges:
                tabu_edges.pop(0)
            temp=path[i]
            path[i]=path[j]
            path[j]=temp
        temperature*=temp_coeff
    return path


def add_tabu_edges(tabu_list, max_edges, path):
    prev=-1
    for v in path:
        if prev==-1:
            prev=v
            continue
        if(numpy.random.randint(100)<50):
            tabu_list.append((prev,v))
        if(len(tabu_list)>max_edges):
            tabu_list.pop(0)
        prev=v
    return

import re
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
'''
competition_results=[]
directory = 'Competion'
files=sorted(os.listdir(directory),key=numericalSort)
for filename in files[77:]:
    f=os.path.join(directory,filename)
    if os.path.isfile(f):
        node_count,distances = openFile(f)
        path=[]
        start=time.time()
        path=nearestNeighbor(distances)
        path=simulated_annealing(distances,path)
        #path=two_opt(distances,path)
        end=time.time()
        competition_results.append(""+str(calculate_cost(path,distances))+","+str(end-start))
        result=""+str(calculate_cost(path,distances))+","+str(end-start)
        with open("competition_results.out",'a') as g:
            sys.stdout=g
            print(result)

'''

node_count,distances = openFile("Competion\\tsp-problem-1000-100000-100-5-1.txt")
path=[]
start=time.time()
path=nearestNeighbor(distances)
path=simulated_annealing(distances,path)
path=two_opt(distances,path)
end=time.time()
print(end-start)
print(str(calculate_cost(path,distances)))
