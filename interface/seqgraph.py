class Sequence:
	def __init__(self, snapshot):
		self.sequences = snapshot["sequence"]
		self.n = snapshot["n"]
	
	def getSeq(self, index):
		return self.sequences[index]

	def getSeqIndices(self, index):
		sequence = self.getSeq(index)
		l = []
		for i in range(len(sequence)):
			l.append(sequence[str(i)]['index'])
		return l

	def getLastSeq(self):
		if self.n == 0:
			return []
		return self.getSeq(self.n)


class Graph:
	def __init__(self):
		n = 0