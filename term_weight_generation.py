import pyrebase
import json
import sys
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from word_processing import *

# term is the string to find frequency
# document is a list of terms which collectively represent a document
def calculateTF(term, document):
	frequency = 0
	for doc_term in document:
		if wordSemanticEqual(term, doc_term):
			frequency += 1
	return float(frequency) / len(document)

# term is the string to find frequency
# document group is a list of term lists
def calculateIDF(term, document_group):
	frequency = 0
	for document in document_group:
		if calculateTF(term, document) > 0:
			frequency += 1
	return math.log(len(document_group) / float(frequency))

def getSubgoalTermWeight(sequences):
	label_sequences = []
	for key in sequences:
	    nodes = sequences[key]["nodes"]
	    label_sequence = []
	    for node in nodes:
	        label_sequence.append(node["label"])
	    label_sequences.append(" ".join(label_sequence))

	# Extract keywords from labels
	document_group = []
	for label_sequence in label_sequences:
		POS_tag_list = pos_tag(word_tokenize(label_sequence))
		keyword_list = [t[0] for t in POS_tag_list if ("NN" in t[1] or "JJ" in t[1] or t[1] == "VB")]
		document_group.append(keyword_list)

	# Calculate idf for each term and return idf valures
	idf_table = {}
	for document in document_group:
		for term in document:
			if term not in idf_table:
				idf_table[term] = calculateIDF(term, document_group)

	return idf_table

if len(sys.argv) == 1:
	print("USAGE: [Option1: topic] [Option2: problem_num]")
	exit(1)

with open('db-config.json') as db_config_file:    
    config = json.load(db_config_file)

firebase = pyrebase.initialize_app(config)
db = firebase.database()

topic = sys.argv[1]
problem_num = sys.argv[2]

sequences = db.child(topic+"/problems/"+problem_num+"/sequences").get().val()

term_weight = getSubgoalTermWeight(sequences)

# with open('term_weight.json', 'w') as f:
#     json.dump(term_weight, f)

print(term_weight)
