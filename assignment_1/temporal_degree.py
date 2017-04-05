#!/usr/bin/python

from igraph import *
import networkx as nx

import csv
import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from random import randint
import collections




########################################
#Functions
########################################

def create_graph(edgeList):
    G=nx.Graph()    
    for edge in edgeList:
        G.add_edge(edge[0], edge[1])
    return G


def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def temporal_closeness(time_dict):
    clossD = defaultdict(list)
    for t in timeD:
        Gt = create_graph(timeD[t])
        closs = nx.closeness_centrality(Gt) #returns dictionary {'node1':closs1, 'node2': closs2...}
        for key, value in closs.iteritems():
        	clossD[key].append(value)
    for node in clossD:
       clossD[node] = np.mean(clossD[node])

    return clossD


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

def compute_closeness_metric(clossD):    
    rRXf = {}
    clossTupleList = []
    for i in clossD:
        clossTupleList.append((i, clossD[i]))    

    Cl = [int(tup[0]) for tup in sorted(clossTupleList, key=lambda x: x[1], reverse=False)]    

    for f in np.arange(0.05,0.55,0.05):
        #print f
        lastElement = int(f*len(Cl))
        rRXf[f] = float(len(intersect(R[:lastElement], Cl[:lastElement])))/float(len(R[:lastElement]))
    return rRXf

def intersect(a, b):
    return list(set(a) & set(b))
def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'w+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def plot_all_metrics(rRDf, rRCf,rRCLf,rRClTf):

	x = []
	y = []
	yc = []
	ycl = []
	yclt = []	

	rRDf_sorted = collections.OrderedDict(sorted(rRDf.items()))
	rRCf_sorted = collections.OrderedDict(sorted(rRCf.items()))
	rRCLf_sorted = collections.OrderedDict(sorted(rRCLf.items()))
	rRClTf_sorted = collections.OrderedDict(sorted(rRClTf.items()))	
	

	for t in rRDf_sorted:
		x.append(t)
		y.append(rRDf_sorted[t])
		yc.append(rRCf_sorted[t])
		ycl.append(rRCLf_sorted[t])
		yclt.append(rRClTf_sorted[t])	

	plt.scatter(x,y, marker = 'o', s=75, c = "green")
	plt.plot(x,y,'-',color = "green" )	

	plt.scatter(x,yc, marker = 'o', s=75, c = "red")
	plt.plot(x,yc,'-',color = "red" )	

	plt.scatter(x,ycl, marker = 'o', s=75, c = "yellow")
	plt.plot(x,ycl,'-',color = "yellow" )	

	plt.scatter(x,yclt, marker = 'o', s=75, c = "brown")
	plt.plot(x,yclt,'-',color = "brown" )	

	#legend
	p1 = plt.Rectangle((0, 0), 0.1, 0.1, fc="green")
	p2 = plt.Rectangle((0, 0), 0.1, 0.1, fc="red")
	p3 = plt.Rectangle((0, 0), 0.1, 0.1, fc="yellow")
	p4 = plt.Rectangle((0, 0), 0.1, 0.1, fc="brown")	

	plt.legend((p1,p2,p3,p4), ('Degree', 'Clust.Coef.', 'Closeness','Temp.Closeness'), loc='best')	

	plt.grid()
	plt.show()


########################################################################################################33
#Global Variavbles
timeD = {}  # Dictionary with the edgelist per time  {"0":[{1,2},(5,6)...], "1":[(4,7)...]...}
nodesD = [] # Dictionary which contains an inf{} per node

R = load_obj("R10")#

create_edgelist_per_time("data.csv", timeD)      # this could have been done only once. However, it is faster o build the edgelist each time 
clossT = temporal_closeness(timeD)
rRClTf = compute_closeness_metric(clossT)
save_obj(rRClTf, "rRClTf")

#plot rRCFs
rRDf=load_obj("rRDf11")
rRCf = load_obj("rRCf11")
rRCLf = load_obj("rRCLf11")
rRClTf = load_obj("rRClTf")

plot_all_metrics(rRDf, rRCf,rRCLf,rRClTf)


