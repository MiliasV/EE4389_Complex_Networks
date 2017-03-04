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

g = graph.Graph(newlist) #Create graph based on node connections

#Number of Nodes

nodes = g.vcount()
#The total amount of nodes is 244, according with the console the result is 
#243 but python takes into account the 0 value.

#Number of links 

links = g.ecount()

#The total amount of links is 8318, according with the console the result is 
#8317 but python takes into account the 0 value.

#Link density

grDen = graph.Graph.density(g)

#According with the console grDen = 0.282862292963

#Average Degree

avgDeg = (2*links/nodes)

#This formula was taken from her slide 18. According with the console 
#the result is 68.


#the average degree E[D]

avgDegVec = np.average(np.asarray(g.degree()))

#According with the console the average degree vector is 68.4526748971

#the degree variance Var[D]

varDeg = np.var(np.asarray(g.degree()))

#According with the console the variance is 722.469982557

#QUESTION 2

#https://jeremykun.com/2013/08/22/the-erdos-renyi-random-graph/
#https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model

edges = np.array(dataset.iloc[:,[0,1]]).tolist()

gx = graph.Graph(vertex_attrs={"label":vertices}, edges=edges, directed=True)

layout = g.layout("kk")
graph.plot(g, layout = layout)

#Well i decided that the best option to build the graph was the free scale
#because we have a well defined network, that means that we know where each
#node should be connected to each other. The other two graph methods, implied
#that we need to know a probability that a connection can happen and given the 
#data set, we do not have a probability that a connection might happen, we know
#perfectly in which position each node is.

#Question 3

#What is the degree correlation (assortativity)?  What is its physical meaning
degCorrel = g.assortativity_degree(directed=True)

#The degree correlation is equal to 0.118271446119

#Physical meaning.??

#QUESTION 4

#What is the clustering coefficient C?
clustCoef = g.transitivity_undirected(mode="nan")

#According with the console result the clustCoef = 0.4797898838442378

#QUESTION 5

#What is the average hopcount E[H] of the shortest paths between all node 
#pairs?  What is the diameter H max? Well according with her slides this term 
#question resfers to the closeness of the graph

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

#QUESTION 6
#Has this network the small-world property? Justify your conclusion quantitatively.
#Well according with my analysis in question 5 about the hopcount the result
#was around 0.365761267373. Therefore this network has the smallest-world 
#property, she refers to this property that no matter what all nodes are 
#separate from each other by 6 connections, and well our analysis said that 
#we have 0.365761267373.... therefore it  has the small-world property. If you think I am wrong please 
#change it.
#If we use the betweennes then the network does not own the samallest world,
#property, which implies that everyone is connected at least by 6 connection degrees.

#QUESTION 7
#What is the largest eigenvalue (spectral radius) lambda 1 of the adjacency matrix?
#first create the adjacency matrix 
adjMat = g.get_adjacency()  
#Well fucking python do not save the matrix as a variable so I have to create 
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



