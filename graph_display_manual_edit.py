import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import sys
import argparse

G = nx.DiGraph()
def addEdge(x, y):
	if (x, y) in G.edges():
		G[x][y]['weight'] += 1
	else:
		G.add_edge(x, y, weight=1)


def addPath(name, l):
	for i in range(len(l) - 1):
		addEdge(l[i], l[i+1])
		if 'weight' in G.node[l[i+1]]:
			G.node[l[i+1]]['weight'] += 1
		else:
			G.node[l[i+1]]['weight'] = 1

	if 'weight' in G.node[l[0]]:
		G.node[l[0]]['weight'] += 1
	else:
		G.node[l[0]]['weight'] = 1
	print(name, len(G.nodes()))


def removeOutlier(thresh):
	while thresh > 0:
		thresh -= 1
		for (x, y, w) in G.edges(data=True):
			G[x][y]['weight'] -= 1

		flag = True
		while flag:
			flag = False
			for (x, y, w) in G.edges(data=True):
				if G[x][y]['weight'] == 0:
					flag = True
					break
			if flag:
				G.remove_edge(x, y)

	flag = True
	while flag:
		flag = False
		for x in G.nodes():
			if G.degree[x] == 0:
				flag = True
				break
		if flag:
			G.remove_node(x)


def drawGraph(filename):
	weight_lst = list(nx.get_node_attributes(G,'weight').values())

	edges = G.edges()
	weights = [G[u][v]['weight'] for u,v in edges]
	wmax = max(weights)
	wmin = min(weights)
	weights_adj = [(x-wmin+1)/(wmax-wmin+1)*4+1 for x in weights]

	pos = graphviz_layout(G, prog='dot')
	nx.draw(G, pos, with_labels = True, width=weights, node_color = [x for x in nx.get_node_attributes(G,'weight').values()], vmin = min(weight_lst) - max(weight_lst)/2, vmax = max(weight_lst)*2, cmap = plt.cm.get_cmap('Greens'))

	plt.savefig('result/manual/'+filename+'.png')
	plt.show()


def problem1(d):
	addPath("-L_vCy4dytrwYaT9JihE", [0, 1, 2, 3])
	addPath("-La-phq8ER6aTND7piLS", [0, 3])
	addPath("-La5GEWIiOjkQL7nrG_g", [0, 1, 3])
	addPath("-LaFedaxffLrLSXSbiZP", [4, 3])
	addPath("-LaGA_EKEss9o1uMQr0m", [5, 4, 3])
	addPath("-LaKfPTz7crmBuc21KtO", [0, 6, 1, 3, 7])
	addPath("-LaL9cp8eu_b7r_oJpTy", [8, 3, 7])
	addPath("-LaOLGyzk-ArXTdpGIwT", [9, 8, 3, 7])
	addPath("-LaUL-1hXHOxpDWWtve9", [10, 8, 11, 3])
	addPath("-LaYTi9caq25hnNg3eCU", [0, 1, 3])
	addPath("-LarjmjDYAjya_x7Vjjh", [0, 12, 6, 1, 3])
	addPath("-LasLsdcNwa-d_m9qKpy", [13, 0, 3])
	addPath("-LaswrkOG4F31BST0Pg1", [4, 14, 3])
	addPath("-LatUMQ6TjrDT4hXXngC", [0, 15, 1, 3])
	addPath("-Lau3zYPwMSam7AUo01S", [0, 12, 1, 3])
	addPath("-LaxOF4zI0YFYzezp4y0", [0, 1, 3])
	addPath("-LayYy3qQp6t8G0MT_4L", [0, 12, 1])
	addPath("-LaywKxI3bGUMyYmdMb5", [0, 1, 3])
	addPath("-Lb1590P5RjZj13U1C_E", [10, 8, 3, 7])
	addPath("-Lb27oRW9tOeQyqyM1Eo", [13, 1, 3])
	addPath("-Lb7gUCmPqZcdeCX0fzq", [8, 3, 7])

	removeOutlier(d)

	drawGraph("problem1")


def problem2(d):
	addPath("-0", [0, 1, 2, 3, 4, 5])
	addPath("-1", [0, 1, 4])
	addPath("-2", [0, 5])
	addPath("-3", [6, 0, 5])
	addPath("-4", [0, 1, 7])
	addPath("-5", [0, 1, 3, 4])
	addPath("-6", [0, 8, 9, 7, 10, 4, 5])
	addPath("-7", [0, 1, 4, 5])
	addPath("-8", [11, 7, 10])
	addPath("-9", [0, 1, 4, 5])
	addPath("-10", [0, 1, 4, 5])
	addPath("-11", [0, 1, 12, 13, 14, 15, 16, 4, 5])
	addPath("-12", [11, 17, 18, 5])
	addPath("-13", [19, 0, 16, 10, 4])
	addPath("-14", [16, 10, 20, 5])
	addPath("-15", [0, 7, 10, 5])
	addPath("-16", [21, 22, 23, 24, 25, 4, 5])
	addPath("-17", [26, 1, 4])
	addPath("-18", [0, 27, 28, 1, 4, 5])
	addPath("-19", [21, 17, 18, 5])
	addPath("-20", [7, 10, 4, 5])

	removeOutlier(d)

	drawGraph("problem2")


def problem3(d):
	addPath("-L_vHa1a-KgPDeDtiY_0", [0, 1, 2, 3, 4])
	addPath("-La-tycrd9sAIZYwOgJt", [0, 1, 5, 4])
	addPath("-La5KjYIlSwe6SGELnSG", [1, 3, 4])
	addPath("-LaF_qSp0jOn9YP_cRyV", [0, 5, 6, 3, 4])
	addPath("-LaG4mA_vloSoUeC9mtG", [7, 8, 4])
	addPath("-LaKb_6P2MEKMB64MN0K", [0, 9, 10, 1, 5, 7, 4])
	addPath("-LaL5sZfng6xLQcGzCoT", [11, 0, 1, 5, 7, 12, 13, 4])
	addPath("-LaOPRQ9ReDDaGNGwuCi", [1, 7, 13, 4])
	addPath("-LaUP3tqPNPojsbtBBct", [0, 1, 8, 4])
	addPath("-LaYRvHMx03f9ZmxsSnL", [0, 8, 4])
	addPath("-LarhzAGykReZ5umDIJA", [0, 1, 14, 5, 2, 15, 3, 8, 4, 16])
	addPath("-LasS7_2snzez778Ghao", [0, 1, 5, 7, 3, 8, 17, 4])
	addPath("-Lat-CK7dZEAfXHZxzw0", [0, 1, 14, 5, 7, 3, 4])
	addPath("-Latc5wXrTMxr9oxsFPo", [0, 1, 7, 3, 8, 13, 4, 16])
	addPath("-Lau-MwCgKuW93y-Je6_", [18, 19, 0, 1, 2, 3, 8, 20, 4, 16])
	addPath("-LaxE-Q4Z1rxD5Vd5mXN", [18, 7, 8, 4])
	addPath("-LaybdO8YPT6qhH0voqi", [0, 5, 8])
	addPath("-LayvIu60adIUjtIpNno", [0, 1, 5, 3, 13, 4])
	addPath("-Lb18IFyciMmoMoBCkGU", [0, 1, 14, 7, 13, 4])
	addPath("-Lb2H8YdSeodUsbMK0wU", [0, 3])
	addPath("-Lb7bpYuuquJfOejtxcS", [5, 6, 13, 16])

	removeOutlier(d)

	drawGraph("problem3")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('-n', type=int)
	parser.add_argument('-d', type=int, nargs='?', default=0)

	args = parser.parse_args()
	n = args.n
	d = args.d
	if n == 1:
		problem1(d)
	elif n == 2:
		problem2(d)
	elif n == 3:
		problem3(d)