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
import statistics


# create graph from the edgeList
def create_multi_graph(edgeList, is_directed):
    if is_directed==0:
        G=nx.MultiGraph()
    else:
        G = nx.DiGraph() 
    for edge in edgeList:
        G.add_edge(edge[0], edge[1])
    return G
        
    #    if edge not in G.edges():
    #        G.add_edge(edge[0], edge[1], weight = 1)
    #    else:
    #        G[edge[0]][edge[1]]['weight']+=1
    #return G

# create graph from the edgeList
def create_graph(edgeList, is_directed):
    if is_directed==0:
        G=nx.Graph()
    else:
        G = nx.DiGraph() 
    for edge in edgeList:
        G.add_edge(edge[0], edge[1])
    return G

def create_aggr_network(file):
    G=nx.Graph()    

    #create graph from csv
    with open(file, "rt") as csvfile:
        mydata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in mydata:
            if row[0]!="" and row[1]!="" and row[2]!="":    
                vertex1 = int(row[0])
                vertex2 = int(row[1])
                G.add_edge(vertex1,vertex2)
    return G 

def create_aggr_network_multi(file):
    G=nx.MultiGraph()    

    #create graph from csv
    with open(file, "rt") as csvfile:
        mydata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in mydata:
            if row[0]!="" and row[1]!="" and row[2]!="":    
                vertex1 = int(row[0])
                vertex2 = int(row[1])
                G.add_edge(vertex1,vertex2)
    return G 

def create_edgelist_per_time(file): #create edgelist 
    timeD = {}  # Dictionary with the edgelist per time  {"0":[(1,2),(5,6)...], "1":[(4,7)...]...}
    with open(file, "rt") as csvfile:
        mydata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in mydata:
            if row[0]!="" and row[1]!="" and row[2]!="":

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
    path = 'images_qa/' + topic + '/' + label + '.png'
    plt.savefig(path)
    plt.close("all")


def average_dict(dictionary):
    #d=[float(sum(values)) / len(values) for key, values in degree_dictionary.items()]
    numbers = [dictionary[key] for key in dictionary]
    mean_ = statistics.mean(numbers)
    return mean_

def writeToCsv(csvList, topic, file):
    csv_sorted = [csvList[0]]
    csv_sorted.extend(sorted(csvList[1:], key = lambda tup:tup[0]))
    csvfile = file + "/temporalMetrics_"+ topic + ".csv"
    g = open(csvfile, 'w+' ,newline='') 
    csvwriter = csv.writer(g)
    zip(*csv_sorted)
    for row in csv_sorted:
        csvwriter.writerow(row)
    g.close()



def main():
    # My code here
    pass

if __name__ == "__main__":
    main()