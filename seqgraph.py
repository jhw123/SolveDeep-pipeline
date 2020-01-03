def dfs(idx, e_adj, path):
	print(path)
	global v
	v[idx] = True
	for x in e_adj[idx]:
		if x in path:
			global cycle
			cycle = path + [x]
			return False
		else:
			if dfs(x, e_adj, path + [x]) == False:
				return False

	return True

def checkCycle(vmax, e_adj):
	global v
	v = [False for i in range(vmax)]
	for i in range(vmax):
		if v[i] == False:
			if dfs(i, e_adj, [i]) == False:
				return False

class Sequence:
	def __init__(self, snapshot):
		self.sequences = snapshot["sequence"]
		self.n = snapshot["n"]
		self.maxidx = 0

		sum = 0

		for student_num in range(len(self.sequences)):
			sum += len(self.sequences[student_num])
			print(sum)

	def getMaxIdx(self):
		sequences = self.getSeqs()
		l = []
		max_idx = 0
		for student_num in range(len(sequences)):
			sequence = sequences[student_num]
			for i in range(len(sequence)):
				if sequence[str(i)]['index'] > max_idx:
					max_idx = sequence[str(i)]['index']
		self.maxidx = max_idx
		return self.maxidx

	def getNewIdx(self):
		max_idx = self.getMaxIdx()
		self.maxidx = max_idx + 1
		return self.maxidx
	
	def putSeqsIndices(self, seqsindices):
		sequences = self.getSeqs()
		for student_num in range(len(sequences)):
			for i in range(len(sequences[student_num])):
				print(sequences[student_num][str(i)]['index'], seqsindices[student_num][i])
				sequences[student_num][str(i)]['index'] = seqsindices[student_num][i]

	def getSeqsIndices(self):
		sequences = self.getSeqs()
		indices = []
		for student_num in range(len(sequences)):
			l = []
			sequence = sequences[student_num]
			for i in range(len(sequence)):
				l.append(sequence[str(i)]['index'])
			indices.append(l)
		return indices
	
	def getSeq(self, index):
		return self.sequences[index]
	
	def getSeqs(self):
		return self.sequences

	def getSeqIndices(self, index):
		sequence = self.getSeq(index)
		l = []
		for i in range(len(sequence)):
			l.append(sequence[str(i)]['index'])
		return l

	def getNodeLabels(self, index):
		sequences = self.getSeqs()
		l = []
		for student_num in range(len(sequences)):
			sequence = sequences[student_num]
			for i in range(len(sequence)):
				if sequence[str(i)]['index'] == index:
					l.append((student_num, sequence[str(i)]['node']['label'], sequence[str(i)]['node']['steps']))
		return l

	def checkMerge(self, indices):
		vmax = self.getMaxIdx() + 1

		e_adj = [list() for i in range(vmax)]

		sequences = self.getSeqs()

		for student_num in range(len(sequences)):
			sequence = sequences[student_num]
			for i in range(len(sequence) - 1):
				e_adj[int(sequence[str(i)]['index'])].append(int(sequence[str(i + 1)]['index']))

		for i in indices:
			for j in indices:
				e_adj[i] += e_adj[j]

		for i in range(vmax):
			e_adj[i] = list(set(e_adj[i]))

		if checkCycle(vmax, e_adj) == False:
			global cycle
			print(cycle)
			return cycle

		return []

	def mergeNodes(self, indices):
		sequences = self.getSeqs()
		min_ind = min(indices)

		l = []
		for student_num in range(len(sequences)):
			sequence = sequences[student_num]
			for i in range(len(sequence)):
				if sequence[str(i)]['index'] in indices:
					sequence[str(i)]['index'] = min_ind
		return [min_ind]

	def separateLabel(self, node_idx, student_num):
		sequences = self.getSeqs()
		sequence = sequences[student_num]
		new_indices = [node_idx]
		for i in range(len(sequence)):
			if sequence[str(i)]['index'] == node_idx:
				sequence[str(i)]['index'] = self.getNewIdx()
				new_indices.append(sequence[str(i)]['index'])
		return new_indices
