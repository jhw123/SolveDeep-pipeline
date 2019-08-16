from word_processing import *

def wordSetIntersection(word_set1, word_set2):
    intersection = []
    for word1 in word_set1:
        for word2 in word_set2:
            if wordSemanticEqual(word1, word2):
                intersection.append(word1)
                break

    for word2 in word_set2:
        for word1 in word_set1:
            if wordSemanticEqual(word1, word2):
                intersection.append(word2)
                break

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