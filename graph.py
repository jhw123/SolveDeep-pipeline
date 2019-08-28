class Graph:
	def __init__(self, snapshot):
		self.max_index = snapshot["max_index"]
		self.nodes = snapshot["nodes"]
		self.edges = snapshot["edges"]
		self.heads = snapshot["heads"]
		self.tails = snapshot["tails"]
		self.n = snapshot["n"]
		self.sequences = snapshot["sequences"]

	def get_heads(self):
		return self.heads

	def add_head(self, head_idx):
		if head_idx not in self.heads:
			self.heads.append(head_idx)
		return self.heads

	def get_tails(self):
		return self.tails

	def add_tail(self, tail_idx):
		if tail_idx not in self.tails:
			self.tails.append(tail_idx)
		return self.tails

	def add_edges(self, edge_lst):
		for edge in edge_lst:
			add_edge(edge)
			#self.edges.append([int(edge[0]), int(edge[1])])

	def add_edge(self, edge):
		for e in self.edges:
			if e[0] == edge[0] and e[1] == edge[1]:
				e[2] += 1
				return
		self.edges.append([int(edge[0]), int(edge[1]), 1])
		#self.edges.append([int(edge[0]), int(edge[1])])
		#self.unique_edges()

	def add_nodes(self, node_lst):
		for node in node_lst:
			self.max_index = self.max_index+1
			self.nodes.append({"index": self.max_index, "nodes": [node], "size": 1})
		return self.max_index

	def add_node(self, node):
		self.max_index += 1
		self.nodes.append({"index": self.max_index, "nodes": [node], "size": 1})
		return self.max_index

	def add_sequence(self, sequence):
		self.sequences.append(sequence)

	def get_edges(self):
		return self.edges

	def get_nodes(self):
		return self.nodes

	def get_node(self, idx):
		return self.nodes[int(idx)]

	def get_snapshot(self):
		return {"max_index": self.max_index,
				"nodes": self.nodes,
				"edges": self.edges,
				"heads": self.heads,
				"tails": self.tails,
				"n": self.n,
				"sequences": self.sequences
				}

	def put_snapshot(self, snapshot):
		self.max_index = snapshot["max_index"]
		self.nodes = snapshot["nodes"]
		self.edges = snapshot["edges"]
		self.heads = snapshot["heads"]
		self.tails = snapshot["tails"]
		self.n = snapshot["n"]
		self.sequences = snapshot["sequences"]

	def get_direct_children(self, idx):
		direct_children = []
		for edge in self.edges:
			if(edge[0] == idx):
				direct_children.append(edge[1])
		return direct_children

	def get_subsequences(self, idx, threshold=2):
		ret = []
		#if(self.get_node(idx)["size"] < threshold):
		#	return -1
		direct_children = self.get_direct_children(idx);
		if(len(direct_children) == 0):
			return [[idx]]
		for child in direct_children:
			child_subsequences = self.get_subsequences(child, threshold)
			if(child_subsequences == -1):
				continue
			# If the current cluster includes a tail node, append a subsequence that stops at the current cluster
			# if idx in self.tails:
			# 	ret.append([idx])
			for sub_sequence in child_subsequences:
				sub_sequence.insert(0, idx)
				ret.append(sub_sequence)
		return ret

	def get_idxs(self):
		ret = []
		for node in self.nodes:
			ret.append(node["index"])
		return ret

	def node_to_idx(self, node_group):
		ret = []
		for node in node_group:
			ret.append(node["index"])
		return ret

	def idx_to_node(self, lst, nodes):
		ret = [];
		for idx in lst:
			for node in nodes:
				if(int(node["index"]) == int(idx)):
					ret.append(node)
		return ret

	def addWeightToNodes(self, nodes):
		print(self.nodes)
		for node in nodes:
			print(node)
			node["size"] += 1

	def addSequenceToGraph(self, sequence_nodes, sequence_edges, sequence_alignment, graph_alignment):
		translation = {}
		sequence = {}
		for i in range(len(sequence_alignment)):
			seq_pattern = sequence_alignment[i]
			graph_pattern = graph_alignment[i]
			is_head = str(seq_pattern) == str(sequence_nodes[0]["index"])
			is_tail = str(seq_pattern) == str(sequence_nodes[-1]["index"])

	        # Match: add a subgoal node to an existing cluster
			if seq_pattern != "_" and graph_pattern != "_":
				seq_node = self.idx_to_node([seq_pattern], sequence_nodes)[0]
				if is_head:
					self.add_head(int(graph_pattern))
				if is_tail:
					self.add_tail(int(graph_pattern))
				node_group_node = self.get_node(graph_pattern)

	            # Check if there exists a duplicate label in the cluster
				if not self.checkIfDuplicateLabelExist(seq_node["label"], node_group_node):
					node_group_node["nodes"].append(seq_node)
				
				node_group_node["size"] += 1
				translation[seq_pattern] = graph_pattern
				sequence[seq_pattern] = {}
				sequence[seq_pattern]["index"] = int(graph_pattern)
				sequence[seq_pattern]["node"] = seq_node
	        # Mismatch: do nothing
			elif seq_pattern == "_":
				continue
			# Insertion: add a subgoal node as a new cluster
			else:
				seq_node = self.idx_to_node([seq_pattern], sequence_nodes)[0]
				new_idx = self.add_node(seq_node)
				if is_head:
					self.add_head(new_idx)
				if is_tail:
					self.add_tail(new_idx)
				translation[seq_pattern] = str(new_idx)
				sequence[seq_pattern] = {}
				sequence[seq_pattern]["index"] = new_idx
				sequence[seq_pattern]["node"] = seq_node
		for edge in sequence_edges:
			self.add_edge([ int(translation[str(edge[0])]), int(translation[str(edge[1])]) ])
		self.n += 1
		return sequence

	#print all the infomation about this graph
	def print_nodes(self):
		print("HEAD:", self.heads)
		print("TAIL:", self.tails)
		for node_group in self.nodes:
			print("#"+str(node_group["index"]) + " (" + str(node_group["size"]) + ")")
			for node in node_group["nodes"]:
				print(node["label"])
		for edge in self.edges:
			print(edge)

	#remove duplicate edges in this.edges array
	def unique_edges(self):
		unique_lst = []
		for x in self.edges:
			if x not in unique_lst:
				unique_lst.append(x)
		self.edges = unique_lst

	def checkIfDuplicateLabelExist(self, label, cluster):
		for node in cluster["nodes"]:
			if node["label"] == label:
				return True
		return False

