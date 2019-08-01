# ntlk natural language package for subgoal label comparison
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
lm = WordNetLemmatizer()

import math, textdistance

from gensim.models.keyedvectors import KeyedVectors
print("loading a word2vec model...")
model = KeyedVectors.load_word2vec_format("./models/glove_vectors.txt", binary=False)
print("glove_vectors model is loaded successfully")

# Referred from https://nlpforhackers.io/convert-words-between-forms/ 
from nltk.corpus import wordnet as wn
# Just to make it a bit more readable
WN_NOUN = 'n'
WN_VERB = 'v'
WN_ADJECTIVE = 'a'
WN_ADJECTIVE_SATELLITE = 's'
WN_ADVERB = 'r'

def convertPOS(word, from_pos, to_pos):    
	synsets = wn.synsets(word, pos=from_pos)

	# Word not found
	if not synsets:
		return []
		
	# Get all lemmas of the word (consider 'a'and 's' equivalent)
	lemmas = [l for s in synsets
				for l in s.lemmas()
				if s.name().split('.')[1] == from_pos
					or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)
						and s.name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)]

	# Get related forms
	derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]

	# filter only the desired pos (consider 'a' and 's' equivalent)
	related_noun_lemmas = [l for drf in derivationally_related_forms
								for l in drf[1] 
								if l.synset().name().split('.')[1] == to_pos
									or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)
									and l.synset().name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)]

	# Extract the words from the lemmas
	words = [l.name() for l in related_noun_lemmas]
	len_words = len(words)
	
	# Build the result in the form of a list containing tuples (word, probability)
	result = [(w, float(words.count(w))/len_words) for w in set(words)]
	result.sort(key=lambda w: -w[1])
	
	# return all the possibilities sorted by probability
	return result


SEMANTIC_EQUAL_THRESHOLD = 0.6
def wordSemanticEqual(word1, word2):
	# This is to correctly compare same word in different forms. e.g. substitution & substitute
	if textdistance.hamming.normalized_similarity(word1, word2) > 0.5:
		return True
	else:
	    try:    # Exception occurs when one of parameter words are not in the model
	        if model.similarity(word1, word2) > SEMANTIC_EQUAL_THRESHOLD:
	            return True
	        else:
	            return False
	    except Exception as e:
	    	# print(e, word1, word2)	# This often prints out keyError. e.g. KeyError("word 'u=x+2' not in vocabulary"
	        if(word1 == word2):
	            return True
	        else:
	            return False
