
import networkx as nx
import osmnx as ox
from IPython.display import IFrame
import math
import os
import pickle
from datetime import datetime
import collections
import shapely
import sys 
print(sys.prefix)
#%matplotlib inline
ox.__version__


# download the street network for Piedmont, CA
#G = ox.graph_from_place("Cupertino, California, USA", network_type="drive")
G = 0
if not os.path.isfile('Graph.pkl') or os.path.getsize('Graph.pkl')==0:
    G = ox.graph_from_place("Sunnyvale, California, USA", network_type="drive", buffer_dist=1000) #buffer dist in meters
    with open('Graph.pkl', 'wb') as file:
        print("dumping...")
        # A new file will be created
        pickle.dump(G, file)
with open('Graph.pkl', 'rb') as file:
    print("Dumped. opening..")
    G = pickle.load(file)


#G = pickle.loads('Graph.pkl', 'wb')
    
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
                #print(G.edges(min_node))
                #print(n1, n2)
                continue
            #print(n1, ", ", n2)
            path = edger[n1][n2]##math.sqrt(math.pow(G.nodes[n1]['x']-G.nodes[n2]['x'], 2) + math.pow(G.nodes[n1]['y']-G.nodes[n2]['y'], 2)) ## since node is a class, whats printed out is toString method, and x and y are var
            #print(path)

            if path+dist[n1] < dist[n2]:
                dist[n2] = path+dist[n1]
                prev[n2] = n1
        unvisited.remove(min_node)

    #for n in dist:
        #print(f"n={n}, prev={prev[n]}, dist={dist[n]}")
    
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
            #copy5-17-22
            if n2 not in edger:
                edger[n2] = {}
            edger[n2][n1] = path
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

    #for n in dist:
    #    print(f"n={n}, prev={prev[n]}, dist={dist[n]}")
    
    return prev#, edger

def doublePath(path, edger):
    #print(path)
    for i in range(0, len(path)-1):
        #print(edger[path[i]])
        #print(path[i], path[i+1])
        new_length = edger[path[i]][path[i+1]]*2
        edger[path[i]][path[i+1]] = new_length
        edger[path[i+1]][path[i]] = new_length
    #path is a list of nodes
    #edger is a 2d array of nodes (both ways)

    #function will double everything in edger on the path
#startcoords = 37.337529, -122.050036

def infPath(path, edger):
    #print(path)
    for i in range(0, len(path)-1):
        #print(edger[path[i]])
        #print(path[i], path[i+1])
        new_length = 2147483647/10
        edger[path[i]][path[i+1]] = new_length
        edger[path[i+1]][path[i]] = new_length


def findClosestKey(G, x, y) :
    shortestdist = infinity
    closestKey = -1
    for vertex in G.nodes():
        #print(vertex)
        dist = math.sqrt(math.pow(G.nodes()[vertex]['x']-x, 2) + math.pow(G.nodes()[vertex]['y']-y,2))
        if dist < shortestdist:
            shortestdist = dist
            closestKey = vertex
    print("shortest:", shortestdist, "x,y", G.nodes()[closestKey]['x'], G.nodes()[closestKey]['y'])
    return closestKey
        
#latitude coord(y) comes first actually (swap startx and starty)
#startx = 37.337529

#starty = -122.050036

#endx = 37.337504

#endy = -122.041433

starty = 37.337529

startx = -122.050036

endy = 37.337504

endx = -122.041433
#endcoords = 37.337504, -122.041433

startr = findClosestKey(H, startx, starty)
print("starter", startr)

endr = findClosestKey(H, endx, endy)
print("ender", endr)


#startr = 5104321608#9336135422
#res = dijkstras(H, start = 9336135422)
edger = computeEdger(H)
crossed = []


textfile = open("result"+str(datetime.today().strftime('%Y-%m-%d_%H_%M_%S'))+ ".txt", 'w')
pathed = []
while (len(crossed) < len(H.nodes())):
    res = dijkstrasEdger(H, start=startr, edger=edger)

    arbitrary_end = endr
    
    backwards = []
    backwards.append(arbitrary_end) #Why does this not work?
    point = res[arbitrary_end]
    backwards.append(point) #nvm forgot to append point (not done later)
    
    while point != startr:
        new_point = res[point]
        backwards.append(new_point)
        point = new_point
    
    print("backwardspath:", backwards)
    #doublePath(backwards, edger)
    infPath(backwards, edger)
    res = backwards
    res.reverse()
    
    for key in res:
        if key not in crossed: 
            crossed.append(key)
    
    flag = 0
    for elem in pathed:
        if collections.Counter(elem) == collections.Counter(res) :
            flag = 1
     
    # Check whether list exists or not.   
    if flag == 0:
        for key in res:
            textfile.write(f'{key},')
        textfile.write('\n')
        pathed.append(res)
    else:
        print("DUPE")
        


    #for key in res:
    #    textfile.write(f'{key},')
    #textfile.write('\n')
    

    #print("#############")
textfile.close()

# #Below is copied to for loop
# res = dijkstrasEdger(H, start=startr, edger=edger)
# #res = resarr[0]
# #edger_prev = resarr[1] ##edger version

# #H.nodes()[9336135422])
# #point = res[65502013] #arbitrary end point
# #point = res[272272951] #broken

# #arbitrary_end = 2460823065#4379447067

# arbitrary_end = endr

# backwards = []

# backwards.append(arbitrary_end) #Why does this not work?

# point = res[arbitrary_end]


# backwards.append(point) #nvm forgot to append point (not done later)

# #p1 = res[point]
# #p2 = res[p1]
# #p3 = res[p2]
# #print(p1, p2, p3)

# while point != startr:
#     new_point = res[point]
#     backwards.append(new_point)
#     #print(backwards)
#     point = new_point
# ##print(backwards)

# ##print("#############")
# ##print(edger)
# #doublePath(backwards, edger)

# print("backwardspath:", backwards)
# doublePath(backwards, edger)

# res = backwards
# res.reverse()
# #save path later #EDIT DONE
# print("#############")
# #print(edger)
# #make paths and then double the edges in between's length


# #Seperate edger-> make it param and return it outside to save to repass in


# ##USE PICKLE LATER TO SAVE GRAPH CACHE- SAVE SCC's GRAPH