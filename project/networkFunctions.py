#!/usr/bin/python3

import networkx as nx
import csv
import networkx as nx
import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import collections
from random import randint
from random import choice

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'w+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

# create graph from the edgeList
def create_graph(edgeList):
    G=nx.Graph()    
    for edge in edgeList:
        G.add_edge(edge[0], edge[1])
    return G

# Input file rows: vertexId-1, vertexId-2, timestamp
# Output: Dictionary with the edgelist per time
def create_edgelist_per_time(file): #create edgelist 
    timeD = {}  # Dictionary with the edgelist per time  {"0":[(1,2),(5,6)...], "1":[(4,7)...]...}
    with open(file, "rb") as csvfile:
        mydata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in mydata:
            vertex1 = int(row[0])
            vertex2 = int(row[1])
            t = int(row[2])
        
            # Create edgelist per time - Adding one edge at a time
            if t in timeD:
                timeD[t].append((vertex1, vertex2))
            else:
                timeD[t]=[]
                timeD[t].append((vertex1, vertex2))
    return timeD

# Assign randomly the timestamps in range (1,maxTime)
def create_edgelist_per_random_time(file, maxTime): #create edgelist 
    timeD = {}  # Dictionary with the edgelist per time  {"0":[{1,2},(5,6)...], "1":[(4,7)...]...}
    with open(file, "rb") as csvfile:
        mydata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in mydata:
            vertex1 = int(row[0])
            vertex2 = int(row[1])
            t = randint(1,maxTime)
        
            # Create edgelist per time - Adding one edge at a time
            if t in timeD:
                timeD[t].append((vertex1, vertex2))
            else:
                timeD[t]=[]
                timeD[t].append((vertex1, vertex2))
    return timeD


def plot_Dict(d, err, mycolor):
    for t in d:
        #plt.scatter(t,d[t], color = mycolor, s=50)
        plt.errorbar(t, d[t], err[t],  fmt='o', color=mycolor)

# Create all links from all timestamps
def create_aggr_network(file):
    G=nx.Graph()    
    #create graph from csv
    with open(file, "rb") as csvfile:
        mydata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in mydata:
            vertex1 = int(row[0])
            vertex2 = int(row[1])
            G.add_edge(vertex1,vertex2)
    return G   

def intersect(a, b):
    return list(set(a) & set(b))

def temporal_degree(time_dict):
    for t in range(1,max(timeD)+1):
        Gt = create_graph(timeD[t])
        tempDegreeList = list(Gt.degree(Gt.nodes()).values())
        print(tempDegreeList)

def compute_closeness_metric(clossD):    

    for i in clossD:
        clossTupleList.append((i, clossAgg[i]))    
    Cl = [int(tup[0]) for tup in sorted(clossTupleList, key=lambda x: x[1], reverse=True)]    

    for f in np.arange(0.05,0.55,0.05):
        #print f
        lastElement = int(f*len(Cl))
        rRXf[f] = float(len(intersect(R[:lastElement], Cl[:lastElement])))/float(len(R[:lastElement]))
    return rRXf


def main():
    # My code here
    pass

if __name__ == "__main__":
    main()