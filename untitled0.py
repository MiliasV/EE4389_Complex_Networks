

import numpy as np
import igraph as graph
import pandas as pd
from scipy.stats import itemfreq






dataset = pd.read_csv('primary school data.csv')
#QUESTION 1
#What is the number of nodes N, the number of links L, the link density p, the 
#average degree E[D] and the degree variance Var[D]?

#Number of Nodes

nodes = len(dataset.node1.unique())


#Nodes = 240, count unique symbols in first array.


#Number of links?

links = dataset['node1'].count()

#Number of links 125774

#Link density?? I am supposed that she might mean, How many average link per 
#node do we have?

linkDen = float(links/nodes)

#Link density = 527

#Average Degree, According with her slide #18 of the first class follow the 
#formula that said AverageDegree=(2*links)/nodes

avgDeg = (2*links)/nodes

#The Average Degree is 1053


#The last value she wants to know the variance of the degree.

degVec = itemfreq(dataset['node1'])

degVar = np.var(degVec[1])

# The degree variance is degVar = 121104.0

#QUESTION 2

#https://jeremykun.com/2013/08/22/the-erdos-renyi-random-graph/
#https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model
vertices = [i for i in range(239)]
edges = np.array(dataset.iloc[:,[0,1]]).tolist()

g = graph.Graph(vertex_attrs={"label":vertices}, edges=edges, directed=True)

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

#The degree correlation is equal to 0.07174392214752584

#Physical meaning.??

#QUESTION 4

#What is the clustering coefficient C?
clustCoef = g.transitivity_undirected(mode="nan")

#According with the console result the clustCoef = 0.4797898838442378

#QUESTION 5

#What is the average hopcount E[H] of the shortest paths between all node 
#pairs?  What is the diameter H max? Well according with her slides this term 
#question resfers to the betweenness of the graph

betnGr = g.betweenness() #array with the betweenness property for each link
avgBetGr = np.average(betnGr)#average result of the betweenness array
maxBet = np.nanmax(betnGr) #max value of the betweenness array.

#diamHop = g.get_diameter(directed="True",unconn="True",weights="None")
#avgHop = g.get_all_shortest_paths(vertices,to="None",mode="ALL") 
#I try the code with the line from above, got the same result,
#just in case that you doubt about the method.

#according with the console the average hopcount is 89.086419753086403
#the max diameter according with the array is 401.240452195

#QUESTION 6
#Has this network the small-world property? Justify your conclusion quantitatively.
#Well according with my analysis in question 5 about the hopcount the result
#was around 89. Therefore this network does not has the smallest-world 
#property, she refers to this property that no matter what all nodes are 
#separate from each other by 6 connections, and well our analysis said that 
#we have 89.... therefore it does not has it. If you think I am wrong please 
#change it.

#QUESTION 7
#What is the largest eigenvalue (spectral radius) lambda 1 of the adjacency matrix?
#first create the adjacency matrix 
adjMat = g.get_adjacency()  
#Well fucking python do not save the matrix as a variable so I have to create 
#another matrix to read the value !! =/
adjMatRead = np.array(adjMat.data)
eigVec = np.linalg.eigvals(adjMatRead)
maxEig = np.amax(eigVec)
#Well i got the the max eigenvalue from the matrix is 0. 
#QUESTION 8
lapVal = g.laplacian(normalized=False)
eigVector = np.linalg.eigvals(lapVal)
eigSort = np.sort(eigVector)
#I create the laplacian matrix, I use normalized = false, because if it is true
#the laplacian matrix is only with 0 or 1 values, it does not tell us anything
#then I extract the eigenvalue vector and sort it to identify the second smallest value
#according with my console the second smallest eigenvalue is 1.0. 




