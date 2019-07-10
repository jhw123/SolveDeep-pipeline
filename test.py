import unittest
from termcolor import colored
from graphAlignOperation import *

TEST_CNT = 0

def checkSubgoalSimilarity(label1, label2, expectation):
	global TEST_CNT

	TEST_CNT += 1
	print colored("---TEST ("+str(TEST_CNT)+")---", 'yellow')
	print("Compare: '"+label1+"' & '"+label2+"'")
	similarity = computeSubgoalLabelSimilarity({"label": label1}, {"label": label2})
	if similarity < expectation:
		print colored("FAIL", 'red'), "- expectation: "+str(expectation)+" actual: "+str(similarity)
		return False
	print colored("PASS", 'green'), "- difference: "+str(expectation-similarity)
	return True

class CustomTests(unittest.TestCase): 
	def test_similarity(self):
		print("TEST_SIMILARITY")
		test_subgoals = [["use integration by substitution for simpler form", "substitute variable to simplify expression", 0.5],
						["substitute variable to simplify expression", "substitute variable to simplify expression", 1.0],
						["solve indefinite integral for u", "solve expression", 0.5],
						["calculate the integral", "calculate the solution with integration", 0.5],
						["expand the expression", "expand the expression further with the common factor", 1.0],
						["integrate the function", "integrate the polynomial", 0.5],
						["substitute variable to simplify expression", "substitute to use substitution integration", 0.5],
						["replace x using u=x+2", "substitute the variable", 0.5]]
		for [label1, label2, expectation] in test_subgoals:
			checkSubgoalSimilarity(label1, label2, expectation)

if __name__ == '__main__':  
	unittest.main()