import networkx as nx
import osmnx as ox
from IPython.display import IFrame
import math

G = ox.graph_from_place("Santa Clara County, California, USA", network_type="drive")
with open('Graph.pkl', 'wb') as file:
      
    # A new file will be created
    pickle.dump(G, file)