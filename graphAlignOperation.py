from graph import Graph
from sequence_align import *
from word_processing import *
from wordSet import *
from statistics import stdev, variance

# ntlk natural language package for subgoal label comparison
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer, LancasterStemmer
lm = WordNetLemmatizer()
ls = LancasterStemmer()

from gensim.models.keyedvectors import KeyedVectors
print("loading a word2vec model...")
model = KeyedVectors.load_word2vec_format("./models/glove_vectors.txt", binary=False)
print("glove_vectors model is loaded successfully")
import numpy as np
import scipy

import re

regex = re.compile('[^a-zA-Z]')

# Load the subgoal term weight file
import json
with open('./term_weight/term_weight_Oxford17.json') as term_weight_file:    
    term_weight = json.load(term_weight_file)

def calcTermWeight(term):
    try:
        return term_weight[ls.stem(term)] + 1
    except Exception as e:
        return 4.0          # add 3.0 for a term that is not in the term_weight. we add high score because being not
                            # in the term_weight means the term is not frequently used by others.

def findTargetSimilarityGraphSequence(nodes, edgs, G, threshold, targetSimilarity=2.0):
    node_group_idx = G.get_idxs()
    node_group_head = G.get_heads()
    nodes_idx = getIndexesOfNodes(nodes)
    min_diff = 100
    min_seq1 = []
    min_seq2 = []
    for head in node_group_head:
        thres = threshold
        node_group_subsequences = G.get_subsequences(head, thres)
        while(node_group_subsequences == -1 or len(node_group_subsequences) == 0):
            thres -= 1
            node_group_subsequences = G.get_subsequences(head, thres)
        if(node_group_subsequences == -1):
            continue
        for subsequence in node_group_subsequences:
            match = alignGlobal(nodes_idx, subsequence, globalAlignmentScoreFunc, nodes, G.get_nodes())
            # print(match[2])
            if(abs(match[2] - targetSimilarity) < min_diff):
                min_diff = abs(match[2] - targetSimilarity)
                min_seq1 = match[0]
                min_seq2 = match[1]
    return [min_diff, min_seq1, min_seq2]

def findMostSimilarGraphSequence(nodes, edges, G, threshold):
    # print(nodes)
    node_group_idx = G.get_idxs()
    node_group_head = G.get_heads()
    nodes_idx = getIndexesOfNodes(nodes)
    max_val = -1
    max_seq1 = []
    max_seq2 = []
    for head in node_group_head:
        thres = threshold
        node_group_subsequences = G.get_subsequences(head, thres)
        while(node_group_subsequences == -1 or len(node_group_subsequences) == 0):
            thres -= 1
            node_group_subsequences = G.get_subsequences(head, thres)
        if(node_group_subsequences == -1):
            continue
        for subsequence in node_group_subsequences:
            match = alignGlobal(nodes_idx, subsequence, globalAlignmentScoreFunc, nodes, G.get_nodes())
            # print(match[2])
            if(match[2] > max_val):
                max_val = match[2]
                max_seq1 = match[0]
                max_seq2 = match[1]
    print("------------------------")
    print("max_val: ", max_val)
    for i in range(len(max_seq1)):
        print("-------")
        if max_seq1[i] != '_':
            print("seq1: ", nodes[int(max_seq1[i])]['label'], nodes[int(max_seq1[i])]['steps'])
        else:
            print("seq1: _")

        if max_seq2[i] != '_':
            graph_node = G.get_node(int(max_seq2[i]))
            for j in range(len(graph_node['nodes'])):
                print("seq2: ", graph_node['nodes'][j]['label'], graph_node['nodes'][j]['steps'])
        else:
            print("seq2: _")
    return [max_val, max_seq1, max_seq2]

MATCH_THRESHOLD = 0.5
def globalAlignmentScoreFunc(node_idx, node_group_idx, nodes, node_group):
    chosen_nodes = getNodesForIndexes([node_idx], nodes)[0]
    chosen_node_group = getNodesForIndexes([node_group_idx], node_group)[0]["nodes"]
    similarity = computeSimilarityBetweenSubgoalAndCluster(chosen_nodes, chosen_node_group)

    return similarity - MATCH_THRESHOLD
    if(similarity > MATCH_THRESHOLD):
        return similarity
    else:
        return -1 * similarity

def computeSimilarityBetweenSubgoalAndCluster(node, nodes):
    score = 0
    similarities = []
    for each_node in nodes:
        similarity = computeSubgoalLabelSimilarity(each_node, node)
        similarities.append(similarity)
        score += pow(similarity, 2)
    score /= len(nodes)
    # print(stdev(similarities))
    return score

def convertTagListToNoun(POS_tag_list):
    word_list = []
    for tag in POS_tag_list:
        if "NN" in tag[1]:
            word_list.append(tag[0])
        elif "FW" in tag[1]:
            word_list.append(tag[0])
        elif "VB" in tag[1]:
            word_list.append(tag[0])
            # try:
            #     word_list.append(convertPOS(tag[0], 'v', 'n')[0][0])
            # except Exception as e:
            #     word_list.append(tag[0])
        elif "JJ" in tag[1]:
            word_list.append(tag[0])
            # try:
            #     word_list.append(convertPOS(tag[0], 'a', 'n')[0][0])
            # except Exception as e:
            #     word_list.append(tag[0])
    return word_list


def subgoalTokenizer(s):
    POS_tag_list = pos_tag(word_tokenize(s))
    word_list = convertTagListToNoun(POS_tag_list)

    # return [lm.lemmatize(regex.sub(' ', w)) for w in word_list if w.replace('\'', '').isalpha()]

    word_set = []
    for w in word_list:
        if w.replace('\'', '').isalpha():
            if '\'' in w:
                word_set += subgoalTokenizer(regex.sub(' ', w))
            else:
                word_set.append(lm.lemmatize(w))
    return word_set

def computeCosineSimilarity(s1, s2):
    ws1 = subgoalTokenizer(s1)
    ws2 = subgoalTokenizer(s2)
    vector_1 = np.mean([model[word] * calcTermWeight(word) for word in ws1 if word in model],axis=0)
    vector_2 = np.mean([model[word] * calcTermWeight(word) for word in ws2 if word in model],axis=0)
    cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
    return round((1-cosine), 4)

def computeSubgoalLabelSimilarity(node1, node2):
    # Fast comparison for identical labels
    if(node1["label"] == node2["label"]):
        return 1.0

    return computeCosineSimilarity(node1["label"], node2["label"])


def getIndexesOfNodes(node_array):
    ret = []
    for node in node_array:
        ret.append(node["index"])
    return ret

def getNodesForIndexes(lst, nodes):
    ret = [];
    for idx in lst:
        for node in nodes:
            if(int(node["index"]) == int(idx)):
                ret.append(node)
    return ret