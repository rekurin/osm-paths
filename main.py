
import networkx as nx
import osmnx as ox
from IPython.display import IFrame
import math

#%matplotlib inline
ox.__version__


# download the street network for Piedmont, CA
G = ox.graph_from_place("Cupertino, California, USA", network_type="drive")

# # plot the street network with ???folium???
#m1 = ox.plot_graph_folium(G, popup_attribute="name", weight=2, color="#8b0000")


H = nx.DiGraph(G)

m1 = ox.plot_graph_folium(G, popup_attribute="name", weight=2, color="#8b0000")

# save as html file then display map as an iframe
filepath = "data/graph.html"
m1.save(filepath)
IFrame(filepath, width=600, height=500)

nodes = G.nodes()
#print(G)
#print(H)

#print(G.nodes()[10758633958]) #.nodes() is the same??
#print(H.edges(8611375192))  #.edges() is a function -given one node, list of those connections, give nothing, all connections
infinity = float("inf")

def dijkstras(G, start):
    dist = {}
    prev = {} #aka shortest known path
    edger = {}
    for vertex in G.nodes():
        dist[vertex] = infinity
        prev[vertex] = -1 ##undefined
        for e in G.edges(vertex):
            n1 = vertex
            n2 = e[1]
            if n1 == n2:
                #print(G.edges(min_node))
                #print(n1, n2)
                continue
            path = math.sqrt(math.pow(G.nodes[n1]['x']-G.nodes[n2]['x'], 2) + math.pow(G.nodes[n1]['y']-G.nodes[n2]['y'], 2)) ## since node is a class, whats printed out is toString method, and x and y are var
            if n1 not in edger:
                edger[n1] = {}
            edger[n1][n2] = path
    dist[start] = 0
    
    unvisited = list(G.nodes())
    while unvisited:
        min_node = None
        for node in unvisited:
            if min_node is None:
                min_node = node
            elif dist[node] < dist[min_node]:
                min_node = node

        for edge in G.edges(min_node):
            #n1 = G.nodes[edge[0]] #current
            n1 = min_node #int
            n2 = edge[1] #int
            if n1 == n2:
                print(G.edges(min_node))
                print(n1, n2)
                continue
            #print(n1, ", ", n2)
            path = edger[n1][n2]##math.sqrt(math.pow(G.nodes[n1]['x']-G.nodes[n2]['x'], 2) + math.pow(G.nodes[n1]['y']-G.nodes[n2]['y'], 2)) ## since node is a class, whats printed out is toString method, and x and y are var
            #print(path)

            if path+dist[n1] < dist[n2]:
                dist[n2] = path+dist[n1]
                prev[n2] = n1
        unvisited.remove(min_node)

    for n in dist:
        print(f"n={n}, prev={prev[n]}, dist={dist[n]}")
    
    return prev
def computeEdger(G):
    
    edger = {}
    for vertex in G.nodes():
        for e in G.edges(vertex):
            n1 = vertex
            n2 = e[1]
            if n1 == n2:
                #print(G.edges(min_node))
                #print(n1, n2)
                continue
            path = math.sqrt(math.pow(G.nodes[n1]['x']-G.nodes[n2]['x'], 2) + math.pow(G.nodes[n1]['y']-G.nodes[n2]['y'], 2)) ## since node is a class, whats printed out is toString method, and x and y are var
            if n1 not in edger:
                edger[n1] = {}
            edger[n1][n2] = path
    return edger

def dijkstrasEdger(G, start, edger):
    dist = {}
    prev = {} #aka shortest known path
    #edger = {}

    for vertex in G.nodes():
        dist[vertex] = infinity
        prev[vertex] = -1 ##undefined
        
    dist[start] = 0
    
    unvisited = list(G.nodes())
    while unvisited:
        min_node = None
        for node in unvisited:
            if min_node is None:
                min_node = node
            elif dist[node] < dist[min_node]:
                min_node = node

        for edge in G.edges(min_node):
            #n1 = G.nodes[edge[0]] #current
            n1 = min_node #int
            n2 = edge[1] #int
            if n1 == n2:
                print(G.edges(min_node))
                print(n1, n2)
                continue
            #print(n1, ", ", n2)
            path = edger[n1][n2]##math.sqrt(math.pow(G.nodes[n1]['x']-G.nodes[n2]['x'], 2) + math.pow(G.nodes[n1]['y']-G.nodes[n2]['y'], 2)) ## since node is a class, whats printed out is toString method, and x and y are var #NO
            #print(path)

            if path+dist[n1] < dist[n2]:
                dist[n2] = path+dist[n1]
                prev[n2] = n1
        unvisited.remove(min_node)

    for n in dist:
        print(f"n={n}, prev={prev[n]}, dist={dist[n]}")
    
    return prev#, edger



startr = 9336135422
#res = dijkstras(H, start = 9336135422)
edger = computeEdger(H)
res = dijkstrasEdger(H, start = 9336135422, edger=edger)
#res = resarr[0]
#edger_prev = resarr[1] ##edger version

#H.nodes()[9336135422])
#point = res[65502013] #arbitrary end point
#point = res[272272951] #broken
point = res[4379447067]

backwards = []

backwards.append(4379447067)
#p1 = res[point]
#p2 = res[p1]
#p3 = res[p2]
#print(p1, p2, p3)

while point != startr:
    new_point = res[point]
    backwards.append(new_point)
    #print(backwards)
    point = new_point
print(backwards)

#save path later #EDIT DONE

#make paths and then double the edges in between's length


#Seperate edger-> make it param and return it outside to save to repass in
