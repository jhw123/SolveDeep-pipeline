import unittest
from termcolor import colored
from graphAlignOperation import *

TEST_CNT = 0

def checkSubgoalSimilarity(label1, label2, expectation, config):
	global TEST_CNT

	TEST_CNT += 1
	print(colored("---TEST ("+str(config)+"-"+str(TEST_CNT)+")---", 'yellow'))
	print("Compare: '"+label1+"' & '"+label2+"'")
	similarity = computeSubgoalLabelSimilarity({"label": label1}, {"label": label2}, config)
	if similarity < expectation:
		print(colored("FAIL", 'red'), "- expectation: "+str(expectation)+" actual: "+str(similarity))
		return False
	else:
		print(colored("PASS", 'green'), "- difference: "+str(expectation-similarity))
		return True

class CustomTests(unittest.TestCase):
	test_subgoals = [["use integration by substitution for simpler form", "substitute variable to simplify expression", 0.5],
					["substitute variable to simplify expression", "substitute variable to simplify expression", 1.0],
					["solve indefinite integral for u", "solve expression", 0.5],
					["calculate the integral", "calculate the solution with integration", 0.5],
					["expand the expression", "expand the expression further with the common factor", 1.0],
					["integrate the function", "integrate the polynomial", 0.5],
					["substitute variable to simplify expression", "substitute to use substitution integration", 0.5],
					["replace x using u=x+2", "substitute the variable", 0.5]]

	def test_similarity_old(self):
		print("TEST_SIMILARITY: OLD")
		correct_num = 0
		total_num = 0
		global TEST_CNT
		TEST_CNT = 0
		for [label1, label2, expectation] in self.test_subgoals:
			if checkSubgoalSimilarity(label1, label2, expectation, 'old') == True:
				correct_num += 1
			total_num += 1
		print("%d / %d \n" % (correct_num, total_num))

	def test_similarity_Oxford17(self):
		print("\nTEST_SIMILARITY: OXFORD17")
		correct_num = 0
		total_num = 0
		global TEST_CNT
		TEST_CNT = 0
		for [label1, label2, expectation] in self.test_subgoals:
			if checkSubgoalSimilarity(label1, label2, expectation, 'Oxford17') == True:
				correct_num += 1
			total_num += 1
		print("%d / %d \n" % (correct_num, total_num))

if __name__ == '__main__':  
	unittest.main()