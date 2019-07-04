import unittest
from graphAlignOperation import *

def checkSubgoalSimilarity(label1, label2, expectation):
	similarity = computeSubgoalLabelSimilarity({"label": label1}, {"label": label2})
	return similarity

class CustomTests(unittest.TestCase): 
	def test_runs(self):
		test_subgoals = [["use integration by substitution for simpler form", "substitute variable to simplify expression", 0.6],
						["substitute variable to simplify expression", "substitute variable to simplify expression", 1.0]]
		for [label1, label2, expectation] in test_subgoals:
			self.assertTrue(checkSubgoalSimilarity(label1, label2, expectation) >= expectation)

if __name__ == '__main__':  
	unittest.main()