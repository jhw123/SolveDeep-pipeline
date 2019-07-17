from word_processing import *

def wordSetIntersection(word_set1, word_set2):
    intersection = []
    for word1 in word_set1:
        for word2 in word_set2:
            if wordSemanticEqual(word1, word2):
                intersection.append(word1)
                # if(word1 != word2): # Note that both words (if different) are added to the intersection set
                intersection.append(word2)
                # break # break is removed in order to add all similar words in a same word_set
    return intersection

def checkIfWordSetIsSubset(word_set1, word_set2):
    include_all = True
    for word in word_set1:
        if word not in word_set2:
            include_all = False
            break
    if include_all:
        return True
    return False