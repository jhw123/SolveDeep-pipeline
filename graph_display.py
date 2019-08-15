import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

import json
with open('result/result.json') as result_file:    
    result = json.load(result_file)

G = nx.DiGraph()

for edge in result["edges"]:
	print(edge)
	G.add_edge(edge[0], edge[1])

pos = graphviz_layout(G)
nx.draw(G, pos, with_labels = True)
plt.show()
plt.savefig('result/graph.png')