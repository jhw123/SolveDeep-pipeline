class Graph:
	def __init__(self, snapshot):
		self.max_index = snapshot["max_index"]
		self.nodes = snapshot["nodes"]
		self.edges = snapshot["edges"]
		self.heads = snapshot["heads"]
		self.n = snapshot["n"]

	def get_heads(self):
		return self.heads

	def add_edges(self, edge_lst):
		for edge in edge_lst:
			self.edges.append([int(edge[0]), int(edge[1])])

	def add_edge(self, edge):
		self.edges.append([int(edge[0]), int(edge[1])])
		self.unique_edges()

	def add_nodes(self, node_lst):
		for node in node_lst:
			self.max_index = self.max_index+1
			self.nodes.append({"index": self.max_index, "nodes": [node], "size": 1})
		return self.max_index

	def add_node(self, node, head=False):
		self.max_index += 1
		self.nodes.append({"index": self.max_index, "nodes": [node], "size": 1})
		if(head):
			self.heads.append(self.max_index)
		return self.max_index

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
				"n": self.n
				}

	def put_snapshot(self, snapshot):
		self.max_index = snapshot["max_index"]
		self.nodes = snapshot["nodes"]
		self.edges = snapshot["edges"]
		self.heads = snapshot["heads"]
		self.n = snapshot["n"]

	def get_direct_children(self, idx):
		direct_children = []
		for edge in self.edges:
			if(edge[0] == idx):
				direct_children.append(edge[1])
		return direct_children

	def get_subsequences(self, idx, threshold=2):
		ret = []
		if(self.get_node(idx)["size"] < threshold):
			return -1
		# if(len(self.get_node(idx)["nodes"]) < threshold):
		# 	return -1
		direct_children = self.get_direct_children(idx);
		if(len(direct_children) == 0):
			return [[idx]]
		for child in direct_children:
			child_subsequences = self.get_subsequences(child, threshold)
			if(child_subsequences == -1):
				continue
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
				if(node.index == idx):
					ret.append(node)
		return ret

	#print all the infomation about this graph
	def print_nodes(self):
		print(self.heads)
		for node_group in self.nodes:
			print("#"+str(node_group["index"]))
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


