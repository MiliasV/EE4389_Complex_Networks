#!/usr/bin/python

from igraph import *
import networkx as nx

import csv
import pickle
import time

import matplotlib.pyplot as plt



start = time.time()

##########  Functions
def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'w+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def create_graph(edgeList):
    G=nx.Graph()    
    for edge in edgeList:
        G.add_edge(edge[0], edge[1])
    return G

def create_edgelist_per_time(file): #create edgelist 
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

def plot_It(d):
    for t in d:
        plt.scatter(t,len(d[t]))

###############################################3

#Global Variavbles
timeD = {} #Dictionary with the edgelist per time  {"0":[{1,2},(5,6)...], "1":[(4,7)...]...}
inf = {}  # Dictionary with the infected nodes per time
allInf = [] # List with all the currently infected nodes
l = []
create_edgelist_per_time("data.csv")      # this could have been done only once. However, it is faster o build the edgelist each time 
#save_obj(timeD, "edgelist_dictionary")   #than loading it.
#save_obj(inf, "infected_dictionary")
#timeD = load_obj("edgelist_dictionary")
#inf = load_obj("infected")
allInf.append(67)

# Creating the network topology per time
for t in timeD:

    print(t)

    # if all nodes infected stop
    if len(allInf)==242:
        break
    G = create_graph(timeD[t]) # Create the graph that corresponds to this time
    
    graphs = list(nx.connected_component_subgraphs(G)) # find the connected subgraphs
    
    for subgraph in graphs:
        for node in subgraph.nodes():             # for each node in each connected subgraph
            if node in allInf:                    # check if node is in the infected list and if it is, add all the nodes
                
                #inf[t].extend(subgraph.nodes())   # of the subgraph to the infected list.
                #inf[t] = [x for x in inf[t] if x not in allInf] # put in the infected dictionary only the new infected nodes
                
                allInf.extend(subgraph.nodes())
                allInf = list(set(allInf))
                break
    
    inf[t] = allInf[:] # copy variable, not bind
    l.append((t, len(allInf)))
for i in inf:
    print i, len(inf[i])
#plot_It(inf)
#plt.show()
end = time.time()
print(end - start)

    