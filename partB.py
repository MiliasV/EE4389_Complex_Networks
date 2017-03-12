#!/usr/bin/python

from igraph import *
import networkx as nx

import csv
import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
from random import randint


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

def create_edgelist_per_random_time(file): #create edgelist 
    with open(file, "rb") as csvfile:
        mydata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in mydata:
            vertex1 = int(row[0])
            vertex2 = int(row[1])
            t = randint(1,5846)
        
            # Create edgelist per time - Adding one edge at a time
            if t in timeD:
                timeD[t].append((vertex1, vertex2))
            else:
                timeD[t]=[]
                timeD[t].append((vertex1, vertex2))

def plot_Dict(d, err, mycolor):
    for t in d:
        #plt.scatter(t,d[t], color = mycolor, s=50)
        plt.errorbar(t, d[t], err[t],  fmt='o', color=mycolor)


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

#########################################
## Stimulation of the temporal network
#########################################
for node in range(1, total_number_of_nodes+1):
    #for node in range
    print("node", node)
    allInf = [node] # List with all the currently infected nodes
    inf = {}  # Dictionary with the infected nodes per time
  
    
#    for t in timeD: #Creating the network topology per time
    for t in range(1,max(timeD)+1): #Creating the network topology per time
        #print("time",t)
        # if all nodes infected stop
        if t not in timeD:
            inf[t] = len(allInf[:])
        elif len(allInf)==total_number_of_nodes:
            inf[t] = total_number_of_nodes
        else:
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
    #print nodesD    
end = time.time()
print(end - start)

###############
# Computations#
###############

###################################################################
# (9) Computation of the Average Number of Infected nodes E|I(t)| #
###################################################################
avg = {}
var = {}
for t in nodesD[0]:   # for all times
    #print t
    timeList = [d[t] for d in nodesD]
    avg[t] = np.mean(timeList)
    var[t] = np.std(timeList)

#save_obj(avg, "average9")
#save_obj(var, "var9")
plot_Dict(avg, var ,"red")
#plot_Dict(var, "green")
plt.show()

#############################################
# (10) Ranking of the most influential nodes#
#############################################
#infl = {}
infl =[]
rankVar = (80*total_number_of_nodes)/100
for i in range(0,len(nodesD)):
    infl.append((i, min(k for k in nodesD[i] if nodesD[i][k] >= rankVar))) #[(node, time),..]

R =  [int(tup[0]) for tup in sorted(infl, key=lambda x: x[1])] #Ranking of influence

#save_obj(infl, "RTuple")

#save_obj(R, "R10")

########################################
# (11) Degree & Clustering Coefficient #
########################################
degreeTupleList = []
clustTupleList = []

#TODO: not so many transformations! More efficiently! 
degreeList = list(aggr_graph.degree(aggr_graph.nodes()).values())
clustD = nx.clustering(aggr_graph)

# transform degree list into a sorted ordered list of nodes according to degree
for i in range(0, len(degreeList)-1):
    degreeTupleList.append((i,degreeList[i]))
D =  [int(tup[0]) for tup in sorted(degreeTupleList, key=lambda x: x[1], reverse=True)]
#save_obj(degreeTupleList, "Dtuple10")

print D#print degreeList
#save_obj(D, "D10")

# transform clust. coef. list into a sorted ordered list of nodes according to clust. coef.
for i in clustD:
    clustTupleList.append((i, clustD[i]))
C = [int(tup[0]) for tup in sorted(clustTupleList, key=lambda x: x[1], reverse=True)]
#print clustList
#save_obj(C, "C10")

#######################
# Computation of rRDf #
#######################
rRDf = {}
for f in np.arange(0.05,0.55,0.05):
    print f
    lastElement = int(f*len(D))
    rRDf[f] = float(len(intersect(R[:lastElement], D[:lastElement])))/float(len(R[:lastElement]))
    #print f, rRDf[f]
print rRDf

######################
# Computation of rRCf#
######################
rRCf = {}
for f in np.arange(0.05,0.55,0.05):
    print f
    lastElement = int(f*len(C))
    rRCf[f] = float(len(intersect(R[:lastElement], C[:lastElement])))/float(len(R[:lastElement]))

#save_obj(rRDf, "rRDf11")
#save_obj(rRCf, "rRCf11")


plot_Dict(rRDf, "red")
plot_Dict(rRCf, "green")
plt.show()


################################
# (12) Other centrality metrics#
################################

#Temporal????
#I can also do Betweeness

#########################
#Closeness of Aggregated#
#########################
rRCLf = {}
clossAggTupleList = []

clossAgg = nx.closeness_centrality(aggr_graph)
for i in clossAgg:
    clossAggTupleList.append((i, clossAgg[i]))

Cl = [int(tup[0]) for tup in sorted(clossAggTupleList, key=lambda x: x[1], reverse=True)]

for f in np.arange(0.05,0.55,0.05):
    print f
    lastElement = int(f*len(Cl))
    rRCLf[f] = float(len(intersect(R[:lastElement], Cl[:lastElement])))/float(len(R[:lastElement]))

#save_obj(rRCLf, "rRCf11")

#plot_Dict(rRDf, "red")
#plot_Dict(rRCf, "green")
#plot_Dict(rRCLf, "yellow")

#plt.show()

#################
#Temporal Degree#
#################



################################
# (13) What can be improved?   #
################################

#------------


#####
# C #
#####

aggr_random = create_edgelist_per_random_time("data.csv")
#G2 is exactly the same as Gdata except that the time
#stamps describing when each link appears in G data are randomlized in G2

