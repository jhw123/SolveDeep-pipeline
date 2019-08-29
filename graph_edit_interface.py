import matplotlib
matplotlib.use("GTK3Agg")
from seqgraph import Sequence
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import sys
import json
import argparse
from matplotlib.widgets import TextBox, Button
from ast import literal_eval

result = {}
cur_idx = 20
DG = nx.DiGraph()

class Index(object):
	def prev(self, event):
		global cur_idx
		cur_idx -= 1
		if cur_idx < 0:
			cur_idx = 0
		else:
			drawGraph("-1")

	def next(self, event):
		global cur_idx
		cur_idx += 1
		if cur_idx > 20:
			cur_idx = 20
		else:
			drawGraph("+1")

	def submitHighlight(self, text):
		drawGraph("new")
		student_num = int(text)
		l = Seq.getSeqIndices(student_num)
		l_edges = list(zip(l,l[1:]))
		pos = graphviz_layout(DG, prog='dot')
		nx.draw_networkx_nodes(DG,pos,nodelist=l,node_color='r')
		nx.draw_networkx_edges(DG,pos,edgelist=l_edges,edge_color='r')

	def submitShowLabel(self, text):
		student_num = int(text)
		print("----------------"+text+"----------------")
		labels = Seq.getNodeLabels(student_num)
		t = ''
		for label in labels:
			if cur_idx >= label[0]:
				print(label)

	def submitMerge(self, text):
		ind = literal_eval(text)
		Seq.mergeNodes(ind[0], ind[1])
		drawGraph("new")

	def submitSeparate(self, text):
		ind = literal_eval(text)
		Seq.separateLabel(ind[0], ind[1])
		drawGraph("new")

	def removeTroll(self, text):
		student_num = int(text)

def cleanZero(l):
	global DG
	#for (x, y) in list(zip(l,l[1:])):
	#	DG.remove_edge(x, y)

	for x in l:
		if DG.node[x]['weight'] == 0:
			DG.remove_node(x)

def drawGraph(option):
	global cur_idx
	global problem_num
	global ax
	global DG
	plt.cla()

	if option == "+1":
		l = Seq.getSeqIndices(cur_idx)
		for i in range(len(l) - 1):
			if (l[i], l[i+1]) in DG.edges():
				DG[l[i]][l[i+1]]['weight'] += 1
			else:
				DG.add_edge(l[i], l[i+1], weight=1)

			if 'weight' in DG.node[l[i+1]]:
				DG.node[l[i+1]]['weight'] += 1
			else:
				DG.node[l[i+1]]['weight'] = 1

		if 'weight' in DG.node[l[0]]:
			DG.node[l[0]]['weight'] += 1
		else:
			DG.node[l[0]]['weight'] = 1
	elif option == "-1":
		l = Seq.getSeqIndices(cur_idx + 1)
		for i in range(len(l) - 1):
			DG[l[i]][l[i+1]]['weight'] -= 1
			DG.node[l[i+1]]['weight'] -= 1
		
		DG.node[l[0]]['weight'] -= 1
		cleanZero(l)
	elif option == "new":
		DG.clear()
		for student_num in range(cur_idx + 1):
			l = Seq.getSeqIndices(student_num)
			for i in range(len(l) - 1):
				if (l[i], l[i+1]) in DG.edges():
					DG[l[i]][l[i+1]]['weight'] += 1
				else:
					DG.add_edge(l[i], l[i+1], weight=1)

				if 'weight' in DG.node[l[i+1]]:
					DG.node[l[i+1]]['weight'] += 1
				else:
					DG.node[l[i+1]]['weight'] = 1

			if 'weight' in DG.node[l[0]]:
				DG.node[l[0]]['weight'] += 1
			else:
				DG.node[l[0]]['weight'] = 1

	weight_lst = list(nx.get_node_attributes(DG,'weight').values())

	edges = DG.edges()
	weights = [DG[u][v]['weight'] for u,v in edges]
	wmax = max(weights)
	wmin = min(weights)
	weights_adj = [(x-wmin+1)/(wmax-wmin+1)*4+1 for x in weights]

	pos = graphviz_layout(DG, prog='dot')
	nx.draw(DG, pos, ax=ax, with_labels = True, width=weights, node_color = [x for x in nx.get_node_attributes(DG,'weight').values()], vmin = min(weight_lst) - max(weight_lst)/2, vmax = max(weight_lst)*2, cmap = plt.cm.get_cmap('Greens'))
	num_text = plt.text(0, 0, str(cur_idx))

def showUI():
	global ax
	fig, ax = plt.subplots()
	callback = Index()
	num_text = plt.text(0, 0, str(cur_idx))
	axtextbox_highlight = plt.axes([0.2, 0.05, 0.05, 0.075])
	axtextbox_showlabel = plt.axes([0.3, 0.05, 0.05, 0.075])
	axtextbox_merge = plt.axes([0.4, 0.05, 0.05, 0.075])
	axtextbox_separate = plt.axes([0.5, 0.05, 0.05, 0.075])
	axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
	axnext = plt.axes([0.81, 0.05, 0.1, 0.075])

	textbox_highlight = TextBox(axtextbox_highlight, 'Student #')
	textbox_highlight.on_submit(callback.submitHighlight)

	textbox_showlabel = TextBox(axtextbox_showlabel, 'Node #')
	textbox_showlabel.on_submit(callback.submitShowLabel)

	textbox_merge = TextBox(axtextbox_merge, 'Merge')
	textbox_merge.on_submit(callback.submitMerge)

	textbox_separate = TextBox(axtextbox_separate, 'Separate')
	textbox_separate.on_submit(callback.submitSeparate)

	bprev = Button(axprev, 'Previous')
	bprev.on_clicked(callback.prev)
	bnext = Button(axnext, 'Next')
	bnext.on_clicked(callback.next)
	
	plt.sca(ax)
	drawGraph("new")
	plt.show()

def init():
	global Seq
	Seq = Sequence({"sequence": result["sequences"], "n": 20})
	showUI()


def main():
	global result
	global problem_num
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', type=int)
	args = parser.parse_args()
	problem_num = args.n

	with open('result/result_'+str(problem_num)+'.json') as result_file:
		result = json.load(result_file)
	init()
	#while True:
	#	showCommand()


if __name__ == "__main__":
	main()