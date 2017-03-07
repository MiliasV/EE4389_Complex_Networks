#!/usr/bin/python

from igraph import *
import networkx as nx

import csv
import pickle
import time
import numpy
import matplotlib.pyplot as plt



start = time.time()

########################################
#Functions
########################################
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

def plot_It(d, mycolor):
    for t in d:
        plt.scatter(t,d[t], color = mycolor, s=50)

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

#######################################################################################################################################################################
################################################################################################################################################################

#Global Variavbles
timeD = {}  # Dictionary with the edgelist per time  {"0":[{1,2},(5,6)...], "1":[(4,7)...]...}
nodesD = [] # Dictionary which contains an inf{} per node

create_edgelist_per_time("data.csv")      # this could have been done only once. However, it is faster o build the edgelist each time 
#save_obj(timeD, "edgelist_dictionary")   #than loading it.
#save_obj(inf, "infected_dictionary")
#timeD = load_obj("edgelist_dictionary")
#inf = load_obj("infected")

########################################
#Creation of aggregate graph 
########################################
aggr_graph = create_aggr_network("data.csv")
total_number_of_nodes = aggr_graph.number_of_nodes()

########################################
# Stimulation of the temporal network
########################################
for node in range(1,30 ):#total_number_of_nodes+1):
    #for node in range
    print("node", node)
    allInf = [node] # List with all the currently infected nodes
    inf = {}  # Dictionary with the infected nodes per time
  
    
    for t in timeD: #Creating the network topology per time
        #print("time",t)
        # if all nodes infected stop
        if len(allInf)==total_number_of_nodes:
                inf[t] = total_number_of_nodes
            #break
        G = create_graph(timeD[t]) # Create the graph that corresponds to this time
        
        graphs = list(nx.connected_component_subgraphs(G)) # find the connected subgraphs
        
        for subgraph in graphs:
            for sub_node in subgraph.nodes():             # for each node in each connected subgraph
                if sub_node in allInf:                    # check if node is in the infected list and if it is, add all the nodes
                    
                    #inf[t].extend(subgraph.nodes())   # of the subgraph to the infected list.
                    #inf[t] = [x for x in inf[t] if x not in allInf] # put in the infected dictionary only the new infected nodes
                    
                    allInf.extend(subgraph.nodes())
                    allInf = list(set(allInf))
                    break
        
        inf[t] = len(allInf[:]) # copy variable, not bind
        #seedNodeInf.append(allInf)
    nodesD.append(inf)

end = time.time()
print(end - start)
########################################
# Computations
########################################

############# Computation of the Average Number of Infected nodes E|I(t)|
avg = {}
var = {}
for t in nodesD[0]:   # for all times
    #print t
    timeList = [d[t] for d in nodesD]
    avg[t] = numpy.mean(timeList)
    var[t] = numpy.std(timeList)
#plot_It(avg, "red")
#plot_It(var, "green")
#plt.show()

########################################
# Ranking of the most influential nodes
########################################
#infl = {}
infl =[]
rankVar = (80*total_number_of_nodes)/100
for i in range(0,len(nodesD)):
    #print i, nodesD[i]#, nodesD[i][k]
    #infl[i]

    infl.append((i, min(k for k in nodesD[i] if nodesD[i][k] >= rankVar)))
#for i in nodesD:
#    print i
print infl


########################################
# Degree & Clustering Coefficient
########################################


    