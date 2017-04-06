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
from numbers import Number
import statistics


import networkFunctions as nF

def create_edgelist_per_time(file): #create edgelist 
    timeD = {}  # Dictionary with the edgelist per time  {"0":[(1,2),(5,6)...], "1":[(4,7)...]...}
    with open(file, "rt") as csvfile:
        mydata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in mydata:
            if row[0]!="" and row[1]!="":

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

def plot_Dict(d, mycolor):
    for t in d:
        #plt.plot(t,d[t], '-o',color = mycolor)#, s=50)
        lists = sorted(d.items()) # sorted by key, return a list of tuples

        x, y = zip(*lists) # unpack a list of pairs into two tuples

        plt.plot(x, y,"-o", color=mycolor)

        #plt.errorbar(t, d[t], err[t],  fmt='o', color=mycolor)

def average_degree(degree_dictionary):
    #d=[float(sum(values)) / len(values) for key, values in degree_dictionary.items()]
    numbers = [degree_dictionary[key] for key in degree_dictionary]
    mean_ = statistics.mean(numbers)
    return mean_


timeD = create_edgelist_per_time("data/ruby-on-rails.csv") #edgelist per time
nodeD = {}      # number of nodes per time
edgeD = {}      #number of edges per time
degreeD = {}    #number of avg degree per time
subgD = {}      #number of subgraphs per time
idMaxDegreeD = {}
maxDegreeD = {}
# for each temporal graph
for time in timeD:
    G = nF.create_graph(timeD[time])
    nodeD[time] = len(G.nodes())
    edgeD[time] = len(G.edges())
    degree = nx.degree_centrality(G)
    degreeD[time] = average_degree(degree)
    subgD[time] = len(list(nx.connected_component_subgraphs(G)))
    idMaxDegreeD[time] = max(degree.keys(), key=(lambda key: degree[key]))
    maxDegreeD[time] = degree[idMaxDegreeD[time]]
    print("######### TIME:",time)
    print("Nodes:", len(G.nodes()))
    print("Edges:",len(G.edges()))
    print("degree:",degreeD[time])
    print("subg:",subgD[time])
    print("###########################################")

plt.figure(1)
plot_Dict(nodeD,"red")
plot_Dict(edgeD,"blue")
plt.ylabel('#Nodes and #Edges')
plt.xlabel('Year-Month')
#plt.show()

plt.figure(2)
plot_Dict(degreeD,"green")
plt.ylabel('Average Degree of nodes')
plt.xlabel('Year-Month')
#plt.show()

plt.figure(3)
plot_Dict(subgD,"grey")
plt.ylabel('Number of connected components')
plt.xlabel('Year-Month')

plt.figure(4)
plot_Dict(idMaxDegreeD,"pink")
plt.ylabel('Id with Max degree')
plt.xlabel('Year-Month')

plt.figure(5)
plot_Dict(maxDegreeD,"yellow")
plt.ylabel('Max degree')
plt.xlabel('Year-Month')
plt.show()


# Foolin around
#G = nx.DiGraph()
#G = nx.complete_graph(20)
#G.add_edge(1,2)
#print(nx.degree_centrality(G))
#print(nx.closeness_centrality(G))
#nx.draw_networkx(G)
#plt.show()