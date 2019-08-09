from timeit import default_timer as timer

start = timer()

import os, sys
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer, LancasterStemmer
from word_processing import *
import json
import enchant
from collections import deque

wnl = WordNetLemmatizer()
ls = LancasterStemmer()

# term is the string to find frequency
# document is a list of terms which collectively represent a document
def calculateTF(term, document):
	frequency = 0
	for doc_term in document:
		if wordSemanticEqual(term, doc_term):
			frequency += 1
	return float(frequency) / len(document)


def containsSemanticEqual(term, document):
	for doc_term in document:
		#if wordSemanticEqual(term, doc_term):
		if term == doc_term:
			return True
	return False

# term is the string to find frequency
# document group is a list of term lists
def calculateIDF(term, document_group):
	frequency = 0
	for document in document_group:
		#if calculateTF(term, document) > 0:
		if containsSemanticEqual(term, document):
			frequency += 1
	if frequency == 0:
		print(term)
	return math.log(len(document_group) / float(frequency))


def getSubgoalTermWeight(label_sequences):
	# Extract keywords from labels
	document_group = []
	key_list = []
	for label_sequence in label_sequences:
		POS_tag_list = pos_tag(word_tokenize(label_sequence))
		keyword_list = [ls.stem(t[0]) for t in POS_tag_list if ("NN" in t[1] or "JJ" in t[1] or t[1] == "VB")]
		# print([t for t in POS_tag_list if ("NN" in t[1] or "JJ" in t[1] or t[1] == "VB")])
		document_group.append(keyword_list)
		key_list += keyword_list
	key_list = set(key_list)

	print(key_list)

	print("Tokenizing complete.")

	# Calculate idf for each term and return idf valures
	idf_table = {}
	for term in key_list:
		idf_table[term] = calculateIDF(term, document_group)

	return idf_table


def main():
	sequences = []

	d = enchant.Dict("en_US")

	filecount = 0

	dirname = os.path.dirname(__file__)
	for file in os.listdir('Data'):
		if file.endswith(".txt"):
			print(file)
			filecount += 1
			with open(os.path.join(dirname, 'Data/', file)) as f:
				text = f.read()
				text = " ".join(wnl.lemmatize(w.lower()) for w in word_tokenize(text) \
					if w.isalpha() and d.check(w))
				sequences.append(text)
				# print(text)

	print("Total %d files detected." % filecount)

	term_weight = getSubgoalTermWeight(sequences)

	with open('term_weight.json', 'w') as f:
	    json.dump(term_weight, f, sort_keys=True, indent=4)

	end = timer()
	print(end - start)
	#print(term_weight)


if __name__ == "__main__":
	main()
