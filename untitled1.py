# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 17:48:52 2017

@author: abi
"""


import numpy as np
import igraph as graph
import pandas as pd



"""
VARIABLES 

"""
dataset = pd.read_csv("primary school data.csv") #dataset variable
extCol = np.array(dataset.iloc[:,[0,1]]).tolist() #Extract nodes columns

remDup = list(); #list to store nodes

vertices = [i for i in range(3)]

"""
SEPARATE DUPLICATES
"""


for i in extCol:
    if i not in remDup:
        remDup.append(i)
#list to store sorted unique nodes connections
newlist = sorted(remDup, key = lambda x: x[0]) 


#QUESTION 1
#What is the number of nodes N, the number of links L, the link density p, the 
#average degree E[D] and the degree variance Var[D]?

g = graph.Graph(edges=remDup, directed=False)
layout = g.layout("kk")
#g = graph.Graph(remDup) #Create graph based on node connections


#Number of Nodes

nodes = g.vcount()
#The total amount of nodes is 242. 

#Number of links 

links = g.ecount()

#The total amount of links is 8317.

#Link density

grDen = graph.Graph.density(g)

#According with the console grDen = 0.282862292963


#the average degree E[D]

avgDegVec = np.average(np.asarray(g.degree()))
distr = g.degree_distribution()

#According with the console the average degree vector is 68.4526748971

#the degree variance Var[D]

p = g.degree()
p = p[1:-1]
varDeg = np.var(np.asarray(p))
#According with the console the variance is 708.848780152

#QUESTION 2

#https://jeremykun.com/2013/08/22/the-erdos-renyi-random-graph/
#https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model

edges = np.array(dataset.iloc[:,[0,1]]).tolist()

gx = graph.Graph(vertex_attrs={"label":vertices}, edges=edges, directed=False)
g.degree_distribution()
layout = g.layout("kk")


#Question 3

#What is the degree correlation (assortativity)?  What is its physical meaning
degCorrel = g.assortativity_degree(directed=False)

#The degree correlation is equal to 0.118271446119


#QUESTION 4

#What is the clustering coefficient C?
clustCoef = g.transitivity_undirected(mode="nan")

#According with the console result the clustCoef = 0.4797898838442378

#QUESTION 5

#What is the average hopcount E[H] of the shortest paths between all node 
#pairs?  What is the diameter H max? Well according with her slides this term 
#question resfers to the closeness of the graph
#The average hopcount E[H] of the shortest paths between all node pairs is
#1.73245087617
avgHop = g.average_path_length()
diamG = g.diameter(directed=False,unconn=True,weights=None)
        
betnGr = g.closeness() #array with the closeness property for each link
avgBetGr = np.average(betnGr)#average result of the closeness array
maxBet = np.nanmax(betnGr) #max value of the closeness array.
#Below I compute the betweenness values as well
betwe = g.betweenness()
avgB = np.average(betwe)
maxBe = np.nanmax(avgB)
#diamHop = g.get_diameter(directed="True",unconn="True",weights="None")
#avgHop = g.get_all_shortest_paths(vertices,to="None",mode="ALL") 
#I try the code with the line from above, got the same result,
#just in case that you doubt about the method.

#according with the console the average hopcount is 0.365761267373
#the max diameter according with the array is 0.409475465313



#QUESTION 7
#What is the largest eigenvalue (spectral radius) lambda 1 of the adjacency matrix?
#first create the adjacency matrix 
adjMat = g.get_adjacency()  
# have to create 
#another matrix to read the value !! =/
adjMatRead = np.array(adjMat.data)
eigVec = np.linalg.eigvals(adjMatRead)
maxEig = np.amax(eigVec)
#Well i got the the max eigenvalue from the matrix is 80.2475468894. 
#QUESTION 8

#What is the second smallest eigenvalue of the Laplacian matrix (algebraic connectivity)?
lapVal = g.laplacian(normalized=False)
eigVector = np.linalg.eigvals(lapVal)
eigSort = np.sort(eigVector)
#I create the laplacian matrix, I use normalized = false, because if it is true
#the laplacian matrix is only with 0 or 1 values, it does not tell us anything
#then I extract the eigenvalue vector and sort it to identify the second smallest value
#according with my console the second smallest eigenvalue is 17.035. 


