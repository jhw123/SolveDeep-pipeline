class Sequence:
	def __init__(self, snapshot):
		self.sequences = snapshot["sequence"]
		self.n = snapshot["n"]

	def getMaxIdx(self):
		sequences = self.getSeqs()
		l = []
		max_idx = 0
		for student_num in range(len(sequences)):
			sequence = sequences[student_num]
			for i in range(len(sequence)):
				if sequence[str(i)]['index'] > max_idx:
					max_idx = sequence[str(i)]['index']

		return max_idx
	
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
				sequence[str(i)]['index'] = self.getMaxIdx() + 1
				new_indices.append(sequence[str(i)]['index'])
		return new_indices
