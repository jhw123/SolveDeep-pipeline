from seqgraph import Sequence, Graph
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import sys
import json

problemn = 0

sys.argv[1]
with open('result/result_'+sys.argv[1]+'.json') as result_file:
	result = json.load(result_file)


G = nx.DiGraph()

for edge in result["edges"]:
	G.add_edge(edge[0], edge[1], weight=edge[2])

for node_group in result["nodes"]:
	G.node[node_group["index"]]['weight'] = node_group["size"]

weight_lst = list(nx.get_node_attributes(G,'weight').values())

edges = G.edges()
weights = [G[u][v]['weight'] for u,v in edges]
wmax = max(weights)
wmin = min(weights)
weights_adj = [(x-wmin+1)/(wmax-wmin+1)*4+1 for x in weights]

pos = graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels = True, width=weights, node_color = [x for x in nx.get_node_attributes(G,'weight').values()], vmin = min(weight_lst) - max(weight_lst)/2, vmax = max(weight_lst)*2, cmap = plt.cm.get_cmap('Greens'))

plt.savefig('result/'+sys.argv[1]+'.png')
plt.show()


def showLabels():


def showCommand():
	print("Available commends:")


def main():
	global problemn
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', type=int)
	args = parser.parse_args()
	problemn = args.n
	while True:
		showCommand()



if __name__ == "__main__":
	main()