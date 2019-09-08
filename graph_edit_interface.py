import matplotlib
matplotlib.use("GTK3Agg")
from seqgraph import Sequence
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import matplotlib.gridspec
import sys
import json
import argparse
from matplotlib.widgets import TextBox, Button
from ast import literal_eval
import os.path
import copy

result = {}
pos = {}
cur_idx = 20
max_idx = 20
DG = nx.DiGraph()
sequences_backup = []

gs = matplotlib.gridspec.GridSpec(3, 3, width_ratios=[1, 10, 1], height_ratios=[1, 10, 1])

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
		if cur_idx > max_idx:
			cur_idx = max_idx
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
		global textbox_highlight
		textbox_highlight.set_val("")

	def undo(self, event):
		print("undo")
		global sequences_backup
		print(sequences_backup)
		if sequences_backup:
			Seq.putSeqsIndices(sequences_backup)
			drawGraph("new")

	def submitMerge(self, text):
		global DG_backup
		DG_backup = DG
		ind = literal_eval(text)
		global textbox_merge

		if all(x for x in [Seq.getNodeLabels(idx) for idx in ind]):
			loop_check = Seq.checkMerge(ind)
			# Loop occurrence
			if loop_check:
				text = "Loop: "
				text += ', '.join(map(str, loop_check))
				alert.set_position((0, 0))
				alert.set_text(text)
				alert.set_visible(True)
				textbox_merge.set_val("")
				return

			global sequences_backup
			sequences_backup = Seq.getSeqsIndices()
			print(sequences_backup)

			new_indices = Seq.mergeNodes(ind)
			drawGraph("new")
			pos = graphviz_layout(DG, prog='dot')
			nx.draw_networkx_nodes(DG,pos,nodelist=new_indices,node_color='r')

		textbox_merge.set_val("")

	def submitSeparate(self, text):
		ind = literal_eval(text)
		new_indices = Seq.separateLabel(ind[0], ind[1])
		drawGraph("new")
		pos = graphviz_layout(DG, prog='dot')
		nx.draw_networkx_nodes(DG,pos,nodelist=new_indices,node_color='r')
		global textbox_separate
		textbox_separate.set_val("")

	def updateAnnotation(self, index):
		global fig
		global annot, annotbox
		#annot.set_position(pos[index])
		annot.set_position((0, 0))

		text = ''
		labels = Seq.getNodeLabels(index)
		for label in labels:
			if cur_idx >= label[0]:
				text += "Student " + str(label[0]) + ": " + label[1] + '\n'
				for step in label[2]:
					text += '  . ' + step+'\n'

		annot.set_text(text.rstrip())
		annot.set_visible(True)
		fig.canvas.draw_idle()
		annotbox = annot.get_window_extent()

	def onClick(self, event):
		alert.set_visible(False)
		(x,y) = (event.xdata, event.ydata)
		if not isinstance(x, float) or not isinstance(y, float):
			return

		# Clicked node
		for i in pos.keys():
			dist = (x - pos[i][0]) ** 2 + (y - pos[i][1]) ** 2
			if dist < 200:
				self.updateAnnotation(i)
				return

		annot.set_visible(False)

		# Clicked edge
		for edge in DG.edges():
			if edgeClick((x, y), edge) == True:
				l = []
				l_edges = []
				for student_num in range(cur_idx + 1):
					sequence = Seq.getSeqIndices(student_num)
					for i in range(len(sequence) - 1):
						if sequence[i] == edge[0] and sequence[i + 1] == edge[1]:
							l = list(set(l + sequence))
							l_edges = list(set(l_edges + list(zip(sequence,sequence[1:]))))
							break
				
				drawGraph("")
				nx.draw_networkx_nodes(DG,pos,nodelist=set(l),node_color='r')
				nx.draw_networkx_edges(DG,pos,edgelist=set(l_edges),edge_color='r')
				return
		drawGraph("")
		

def edgeClick(point, edge):
	(x0, y0) = pos[edge[0]]
	(x1, y1) = pos[edge[1]]
	(xp, yp) = point

	dx = x1 - x0
	dy = y1 - y0
	dr2 = float(dx ** 2 + dy ** 2)

	lerp = ((xp - x0) * dx + (yp - y0) * dy) / dr2
	if lerp < 0:
		lerp = 0
	elif lerp > 1:
		lerp = 1

	x = lerp * dx + x0
	y = lerp * dy + y0

	_dx = x - xp
	_dy = y - yp
	square_dist = _dx ** 2 + _dy ** 2
	if square_dist < 20:
		return True
	return False

def cleanZero(l):
	global DG
	#for (x, y) in list(zip(l,l[1:])):
	#	DG.remove_edge(x, y)

	for x in l:
		if DG.node[x]['weight'] == 0:
			DG.remove_node(x)

def drawGraph(option):
	global cur_idx, problem_num, experiment_id
	global fig, ax
	global DG
	refresh()

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
		saveGraph(experiment_id)

	weight_lst = list(nx.get_node_attributes(DG,'weight').values())

	edges = DG.edges()
	weights = [DG[u][v]['weight'] for u,v in edges]
	wmax = max(weights)
	wmin = min(weights)
	weights_adj = [(x-wmin+1)/(wmax-wmin+1)*4+1 for x in weights]

	global pos
	pos = graphviz_layout(DG, prog='dot')
	nx.draw(DG, pos, ax=ax, with_labels = True, width=weights, node_color = [x for x in nx.get_node_attributes(DG,'weight').values()], vmin = min(weight_lst) - max(weight_lst)/2, vmax = max(weight_lst), cmap = plt.cm.get_cmap('Greens'))
	#num_text = plt.text(0.1, 0.9, "Student " + str(cur_idx))
	ax.set_title("Subgoal graph for students 0 ~ " + str(cur_idx))

def refresh():
	global ax, annot, alert
	plt.cla()
	plt.axis('off')
	ax = fig.add_subplot(gs[1, 1])

	annot = ax.annotate("", xy=(0,0), xycoords='axes fraction', bbox=dict(boxstyle='round,pad=0.2', fc='yellow'))
	annot.set_visible(False)
	annot.draggable()
	alert = ax.annotate("", xy=(0,0))
	alert.set_visible(False)

def showUI():
	global fig, ax
	#fig, ax = plt.subplots()
	fig = plt.figure()
	refresh()

	callback = Index()
	fig.canvas.mpl_connect('button_press_event', callback.onClick)
	axtextbox_highlight = plt.axes([0.2, 0.05, 0.05, 0.05])
	axtextbox_merge = plt.axes([0.35, 0.05, 0.05, 0.05])
	axtextbox_separate = plt.axes([0.5, 0.05, 0.05, 0.05])
	axundo = plt.axes([0.6, 0.05, 0.025, 0.05])
	axprev = plt.axes([0.65, 0.05, 0.075, 0.05])
	axnext = plt.axes([0.75, 0.05, 0.075, 0.05])

	global textbox_highlight, textbox_merge, textbox_separate

	textbox_highlight = TextBox(axtextbox_highlight, 'Student #')
	textbox_highlight.on_submit(callback.submitHighlight)

	textbox_merge = TextBox(axtextbox_merge, 'Merge (N#, N#)')
	textbox_merge.on_submit(callback.submitMerge)

	textbox_separate = TextBox(axtextbox_separate, 'Separate (N#, S#)')
	textbox_separate.on_submit(callback.submitSeparate)

	bundo = Button(axundo, 'Undo')
	bundo.on_clicked(callback.undo)
	bprev = Button(axprev, 'Previous')
	bprev.on_clicked(callback.prev)
	bnext = Button(axnext, 'Next')
	bnext.on_clicked(callback.next)
	
	plt.sca(ax)
	drawGraph("new")
	plt.show()

def init():
	global Seq, cur_idx, max_idx
	max_idx = len(result["sequences"]) - 1
	cur_idx = max_idx
	Seq = Sequence({"sequence": result["sequences"], "n": cur_idx})
	showUI()


def main():
	global result
	global problem_num, experiment_id
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', type=int)
	parser.add_argument('-id', type=int)
	args = parser.parse_args()
	problem_num = args.n
	experiment_id = args.id

	with open('result/result_'+str(problem_num)+'.json') as result_file:
		result = json.load(result_file)

	if os.path.isfile('experiment/result_'+str(experiment_id)+'_'+str(problem_num)):
		with open('experiment/result_'+str(experiment_id)+'_'+str(problem_num)) as backup_file:
			backup = json.load(backup_file)
		for i in range(len(backup)):
			for j in range(len(backup[i])):
				result['sequences'][i][str(j)]['index'] = backup[i][str(j)]['index']

	init()
	saveGraph(experiment_id)

def saveGraph(experiment_id):
	with open('experiment/result_'+str(experiment_id)+'_'+str(problem_num), 'w') as outfile:
		json.dump(Seq.getSeqs(), outfile, indent=4)

if __name__ == "__main__":
	main()