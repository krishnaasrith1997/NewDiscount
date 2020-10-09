from __future__ import division
from copy import deepcopy
import random
from priorityQueue import PriorityQueue as PQ
import networkx as nx
import snap
import re
from copy import deepcopy
import random, multiprocessing, os, math, json
import networkx as nx
import matplotlib as plt
import operator

def PageRank(d, e):
    f = open(d)
    s = f.read()
    s1 = re.split('\n', s)
    G1 = snap.PNGraph.New() 
    PRankH = snap.TIntFltH()

    a = re.split(' ', s1[0])

    for i in range(0, int(a[0])):
        G1.AddNode(i)

    for i in range(1, int(a[1]) + 1):
         b = re.split(' ', s1[i])
         b0 = re.sub("\D", "", b[0])
         b1 = re.sub("\D", "", b[1])
         G1.AddEdge(int(b0), int(b1))

    snap.GetPageRank(G1, PRankH)


    EdgePara = dict()

    for i in range(1, int(a[1]) +1):
        c = re.split(' ', s1[i])
        if PRankH[int(c[0])] == 0 and PRankH[int(c[1])] ==0:
            EdgePara[(int(c[0]), int(c[1]))] == 0
            EdgePara[(int(c[1]), int(c[0]))] == 0
        else:
            EdgePara[(int(c[0]), int(c[1]))] = e * PRankH[int(c[0])] / (PRankH[int(c[0])] + PRankH[int(c[1])])
            EdgePara[(int(c[1]), int(c[0]))] = e * PRankH[int(c[1])] / (PRankH[int(c[0])] + PRankH[int(c[1])])

    return EdgePara      

def runIAC (G, S, Ep):
    T = deepcopy(S) # copy already selected nodes

    # ugly C++ version
    i = 0
    while i < len(T):
        for v in G[T[i]]: # for neighbors of a selected node
            if v not in T: # if it wasn't selected yet
                w = G[T[i]][v]['weight'] # count the number of edges between two nodes
                p = Ep[(T[i],v)] # propagation probability
                if random.random() <= 1 - (1-p)**w: # if at least one of edges propagate influence
                    # print T[i], 'influences', v
                    T.append(v)
        i += 1
    return T

def avgIAC (G, S, Ep, I):
    avg = 0
    for i in range(I):
        avg += float(len(runIAC(G,S,Ep)))/I
    return avg


def findCCs(G, Ep):
    # remove blocked edges from graph 
    E = deepcopy(G)
    edge_rem = [e for e in E.edges() if random.random() < (1-Ep[e[0], e[1]])]
    E.remove_edges_from(edge_rem)

    # initialize CC
    CCs = dict() # each component is reflection of the number of a component to its members
    explored = dict(zip(E.nodes(), [False]*len(E)))
    c = -1
    # perform BFS to discover CC
    for node in E:
        if not explored[node]:
            c += 1
            explored[node] = True
            CCs[c] = [node]
            component = list(E[node])
            for neighbor in component:
                if not explored[neighbor]:
                    explored[neighbor] = True
                    CCs[c].append(neighbor)
                    component.extend(E[neighbor].keys())
    return CCs

def GreedyCIC (G, k, Ep, R = 200):

    S = []
    for i in range(k):
        print(i)
        # time2k = time.time()
        scores = {v: 0 for v in G.degree()}
    
        for j in range(R):
            # print j,
            CCs = findCCs(G, Ep)
            for CC in CCs:
                for v in S:
                    if v == (CC):
                        break
                else: # in case CC doesn't have node from S
                    scores[CC] += len(CCs[CC])
        for v in G.node:
            if v in S:
                ba = 0
            else:
                scores[v] = float(scores[v])/R
        #max_v, max_score = max(scores.items(), key = (lambda dk, dv:dv))
        max_v = max(scores.items(), key=operator.itemgetter(1))[0]
        S.append(max_v)
        # print time.time() - time2k
    return S

if __name__ == "__main__":
    import time
    start = time.time()

    G = nx.read_gpickle("C:/Users/Krishna Asrith/Desktop/implementation 1/Graph/MIT.gpickle")
    print ('Read graph G')
    print (time.time() - start)

    d = "C:/Users/Krishna Asrith/Desktop/implementation 1/Graphdata/MIT.txt"

    EdgePara = PageRank(d, 0.1)

    S = GreedyCIC(G, 10, EdgePara)
    print (S)
