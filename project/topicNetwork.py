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

from datetime import date, datetime, timedelta
import monthdelta


# create graph from the edgeList
def create_graph(edgeList, type):
    if type==0:
        G=nx.Graph()
    else:
        G = nx.DiGraph() 
    for edge in edgeList:
        G.add_edge(edge[0], edge[1])
    return G


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

def plot_Dict(d, mycolor, topic, label):
    lists = sorted(d.items()) # sorted by key, return a list of tuples
    x, y = zip(*lists) # unpack a list of pairs into two tuples
    x = list(range(1,len(d)+1))
    plt.figure()
    plt.plot(x, y,"-o", color=mycolor)
    plt.ylabel(label)
    plt.xlabel('Year-Month')
    path = 'images/' + topic + '/' + label + '.png'
    plt.savefig(path)
    plt.close("all")


def average_degree(degree_dictionary):
    #d=[float(sum(values)) / len(values) for key, values in degree_dictionary.items()]
    numbers = [degree_dictionary[key] for key in degree_dictionary]
    mean_ = statistics.mean(numbers)
    return mean_

def main():
    topicList =  ['json', 'angularjs','go', 'reactjs', 'ruby-on-rails', 'swift'] 

    for topic in topicList  :
        data_path = 'data/' + topic + '.csv'
        timeD = create_edgelist_per_time(data_path) #edgelist per time
        nodeD = {}      # number of nodes per time
        edgeD = {}      #number of edges per time
        degreeD = {}    #number of avg degree per time
        subgD = {}      #number of subgraphs per time
        idMaxDegreeD = {}
        maxDegreeD = {}
        clustD = {}     

        # for each temporal graph
        for time in timeD:
            G = create_graph(timeD[time],0)
            if topic=="json":
                save_path = 'images/json/'+ str(time) +'.jpg'
                nx.draw_networkx(G, node_size=2, with_labels=False)
                plt.savefig(save_path)

            nodeD[time] = len(G.nodes())
            edgeD[time] = len(G.edges())
            degree = nx.degree_centrality(G)
            degreeD[time] = average_degree(degree)
            subgD[time] = nx.number_connected_components(G)
            idMaxDegreeD[time] = max(degree.keys(), key=(lambda key: degree[key]))
            maxDegreeD[time] = degree[idMaxDegreeD[time]]
            clustD[time] = nx.average_clustering(G)
            print("######### TIME:",time)
            print("Nodes:", len(G.nodes()))
            print("Edges:",len(G.edges()))
            print("degree:",degreeD[time])
            print("subg:",subgD[time])
            print("###########################################")    
            
        nx.draw_networkx(G, node_size=2, with_labels=False)
        plt.show()
    
        #plot_Dict(nodeD, "red", topic, "nodes")
        #plot_Dict(edgeD, "green", topic, "edges")
        #plot_Dict(degreeD, "grey", topic, "Avgdegree")
        #plot_Dict(subgD, "black", topic, "subgraphs")
        #plot_Dict(idMaxDegreeD, "red", topic, "id")
        #plot_Dict(maxDegreeD, "red", topic, "maxDegree")
        #plot_Dict(clustD, "red", topic, "Avgclust")

if __name__ == "__main__":
    main()

#nx.draw_networkx(G)
#plt.show()