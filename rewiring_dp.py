#!/usr/bin/python

from igraph import *
import networkx as nx

import csv
from igraph import *
import networkx as nx

import csv
import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
import collections
import pickle
from random import randint

from random import choice


########################################
#Functions
########################################\
def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'w+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def plot_infected_per_time(nodesD):
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


def create_edgelist_per_time(file, timeD): #create edgelist 
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

def create_graph(edgeList):
    G=nx.Graph()    
    for edge in edgeList:
        G.add_edge(edge[0], edge[1])
    return G


def degree_rewiring(G,deg): #if deg==0 positive else negative
    tup=[]
    edges = G.edges()
    e1 = choice(edges)
    e2 = choice(edges)
    while e1 == e2:
        e2 = choice(edges)
    tup.append((e1[0],G.degree(e1[0])))
    tup.append((e1[1],G.degree(e1[1])))
    tup.append((e2[0],G.degree(e2[0])))
    tup.append((e2[1],G.degree(e2[1])))

    tup.sort(key=lambda x:x[1])
    if deg==1:
        newEdge1 = (tup[0][0],tup[3][0])
        newEdge2 = (tup[1][0],tup[2][0])
    else:
        newEdge1 = (tup[0][0],tup[1][0])
        newEdge2 = (tup[2][0],tup[3][0])
    if newEdge1 not in G.edges() and newEdge2 not in G.edges():
        G.add_edge(*newEdge1)
        G.add_edge(*newEdge2)
        G.remove_edge(*e1)
        G.remove_edge(*e2)
    return G

def create_edgelist_per_random_time(file): #create edgelist
    timeD={} 
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
    return timeD

def create_edgelist_from_graph_random_time(G,timeD):
    edgeList = G.edges()
    for row in edgeList:
       vertex1 = int(row[0])
       vertex2 = int(row[1])
       t = randint(1,5846)
       # Create edgelist per time - Adding one edge at a time
       if t in timeD:
           timeD[t].append((vertex1, vertex2))
       else:
           timeD[t]=[]
           timeD[t].append((vertex1, vertex2))
    return timeD

def stimulation(timeD):
    nodesD = []
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
    return nodesD
###############################################################################3


Graph = create_aggr_network("data.csv")
total_number_of_nodes = Graph.number_of_nodes()
degAss =  nx.degree_assortativity_coefficient(Graph)

Graph_pos_degree = Graph
Graph_neg_degree = Graph
#creation of G3*
for i in range(1,10000):
    print i
    Graph_pos_degree = degree_rewiring(Graph_pos_degree,0)

print nx.degree_assortativity_coefficient(Graph_pos_degree)

#Creation of G4*
for i in range(1,10000):
    print i
    Graph_neg_degree = degree_rewiring(Graph_neg_degree,1)

print nx.degree_assortativity_coefficient(Graph_neg_degree)

timeDpos = {}
nodeDpos = {}

timeDneg = {}
nodeDneg = {}

timeDrand = {}

#Creation of G2,G3,G4
timeDrand = create_edgelist_per_random_time("data.csv")
timeDpos = create_edgelist_from_graph_random_time(Graph_pos_degree, timeDpos)
timeDneg = create_edgelist_from_graph_random_time(Graph_neg_degree, timeDneg)


nodesDrand = stimulation(timeDrand)
nodeDpos = stimulation(timeDpos)
nodeDneg = stimulation(timeDneg)

save_obj(nodesDrand, "nodesDrand")
save_obj(nodeDpos, "nodesDpos")
save_obj(nodeDneg, "nodesDneg")


plot_infected_per_time(nodesDrand)
plot_infected_per_time(nodeDneg)
plot_infected_per_time(nodeDpos)