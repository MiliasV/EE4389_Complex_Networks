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
from networkx.algorithms.approximation import clique


import networkFunctions as nF

from datetime import date, datetime, timedelta
import monthdelta



def main():
    topicList =  ['json','angularjs','go', 'reactjs', 'ruby-on-rails', 'swift','ember.js', 'meteor'] 
    for topic in topicList  :
        data_path = 'extractedNetworksQuestionAnswer/' + topic + '.csv'
        timeD = nF.create_edgelist_per_time(data_path) #edgelist per time
        nodeD, edgeD, degreeD, subgD, idMaxDegreeD, maxDegreeD, clustD, maxCompD, interactionsD = ({} for i in range(9))
       
        maxCompD = {}
        csvList = []
        csvList.append(["time", "nodes", "edges","avgDegree", "maxDegree", "clustCoef", "subgraphs", "maxComponent", "id_of_max_degree","all_nodes","all_edges"])
        aggr = nF.create_aggr_network(data_path)
        all_nodes = len(aggr.nodes())
        all_edges = len(aggr.edges())

        # for each temporal graph
        for time in timeD:
            G = nF.create_graph(timeD[time],0) # Creation of undirected Graph

            nodeD[time] = len(G.nodes()) #number of nodes
            edgeD[time] = len(G.edges()) #number of edges
            if len(G)>1:
                degree = nx.degree_centrality(G)
                degreeD[time] = nF.average_dict(degree) #average degree centrality
            else:
                degreeD[time] = 'NaN'
            subgD[time] = nx.number_connected_components(G)
            idMaxDegreeD[time] = max(degree.keys(), key =(lambda key: degree[key]))
            maxDegreeD[time] = degree[idMaxDegreeD[time]]
            clustD[time] = nx.average_clustering(G)
            maxCompD[time] = len(max(nx.connected_component_subgraphs(G), key = len))
            csvList.append((int(time), nodeD[time], edgeD[time], degreeD[time], maxDegreeD[time], clustD[time], subgD[time], maxCompD[time], idMaxDegreeD[time], all_nodes, all_edges))
            
        nF.writeToCsv(csvList, topic, "metrics_qa") 


if __name__ == "__main__":
    main()