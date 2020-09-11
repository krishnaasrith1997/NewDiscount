from priorityQueue import PriorityQueue as PQ # priority queue
import networkx as nx
import snap
import re

def Degree(d, e):
    f = open(d)
    s = f.read()
    s1 = re.split('\n', s)
    G1 = snap.PUNGraph.New()

    a = re.split(' ', s1[0])

    for i in range(0, int(a[0])):
        G1.AddNode(i)

    for i in range(1, int(a[1]) + 1):
        b = re.split(' ', s1[i])
        G1.AddEdge(int(b[0]), int(b[1]))

    DegCentr = dict()

    for NI in G1.Nodes():
        DegCentr[NI.GetId()] = snap.GetDegreeCentr(G1, NI.GetId())
	# print "node: %d centrality: %f" % (NI.GetId(), DegCentr)

    # print DegCentr
    EdgePara = dict()

    for i in range(1, int(a[1]) +1):
        c = re.split(' ', s1[i])
        EdgePara[(int(c[0]), int(c[1]))] = e * DegCentr[int(c[0])] / (DegCentr[int(c[0])] + DegCentr[int(c[1])])
        EdgePara[(int(c[1]), int(c[0]))] = e * DegCentr[int(c[1])] / (DegCentr[int(c[0])] + DegCentr[int(c[1])])

    return EdgePara


def NewDiscount(G, k, p):

    S = []
    dd = PQ() # degree discount
    t = dict() # number of adjacent vertices that are in S
    d = dict() # degree of each vertex

    # initialize degree discount
    for u in G.degree():
        d[u] = sum([G[u][v]['weight'] for v in G[u]]) # each edge adds degree 1
        d[u] = len(G[u]) # each neighbor adds degree 1
        dd.add_task(u, -d[u]) # add degree of each node
        t[u] = 0

    # add vertices to S greedily
    for i in range(k):
        u, priority = dd.pop_item() # extract node with maximal degree discount
        S.append(u)
        for v in G[u]:
            if v not in S:
                t[v] += G[u][v]['weight'] # increase number of selected neighbors
                priority = d[v] - 2*t[v] - (d[v] - t[v])*t[v]*p[u, v] # discount of degree
                dd.add_task(v, -priority)
    return S

if __name__ == "__main__":
    import time
    start = time.time()

    G = nx.read_gpickle("C:/Users/Krishna Asrith/Desktop/implementation 1/Graph/retweet.gpickle")
    print ('Read graph G')
    print (time.time() - start)

    d = "C:/Users/Krishna Asrith/Desktop/implementation 1/Graphdata/retweet.txt"

    EdgePara = Degree(d, 1)

    S = NewDiscount(G, 20, EdgePara)
    print (S)
    print (time.time() - start)

