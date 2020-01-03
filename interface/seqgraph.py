class Sequence:
	def __init__(self, snapshot):
		self.sequences = snapshot["sequence"]
		self.n = snapshot["n"]
	
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
					break
		return l

	def getLastSeq(self):
		if self.n == 0:
			return []
		return self.getSeq(self.n)

	def updateSequences(self, cur_idx):
		return None

	def mergeNodes(self, index1, index2, cur_idx):
		if index1 > index2:
			(index1, index2) = (index2, index1)

		sequences = self.getSeqs()
		l = []
		for student_num in range(len(sequences)):
			sequence = sequences[student_num]
			for i in range(len(sequence)):
				if sequence[str(i)]['index'] == index2:
					sequence[str(i)]['index'] = index1

		self.updateSequences(cur_idx)