from graph import Graph
from sequence_align import *
from word_processing import *
from wordSet import *

# ntlk natural language package for subgoal label comparison
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
lm = WordNetLemmatizer()

# Load the subgoal term weight file
import json
with open('term-weight.json') as term_weight_file:    
    term_weight = json.load(term_weight_file)

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
            if(abs(match[2] - targetSimilarity) < min_diff):
                min_diff = abs(match[2] - targetSimilarity)
                min_seq1 = match[0]
                min_seq2 = match[1]
    return [min_diff, min_seq1, min_seq2]

def findMostSimilarGraphSequence(nodes, edges, G, threshold):
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
            print(match[2])
            if(match[2] > max_val):
                max_val = match[2]
                max_seq1 = match[0]
                max_seq2 = match[1]
    return [max_val, max_seq1, max_seq2]

MATCH_THRESHOLD = 0.2
def globalAlignmentScoreFunc(node_idx, node_group_idx, nodes, node_group):
    chosen_nodes = getNodesForIndexes([node_idx], nodes)[0]
    chosen_node_group = getNodesForIndexes([node_group_idx], node_group)[0]["nodes"]
    similarity = computeSimilarityBetweenSubgoalAndCluster(chosen_nodes, chosen_node_group)
    if(similarity > MATCH_THRESHOLD):
        return similarity
    else:
        return -1 * similarity

def computeSimilarityBetweenSubgoalAndCluster(node, nodes):
    score = 0
    for each_node in nodes:
        score += pow(computeSubgoalLabelSimilarity(each_node, node), 2)
    score /= len(nodes)
    return score

def convertTagListToNoun(POS_tag_list):
    word_list = []
    for tag in POS_tag_list:
        if "NN" in tag[1]:
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

def computeSubgoalLabelSimilarity(node1, node2):
    score = 0

    # Fast comparison for identical labels
    if(node1["label"] == node2["label"]):
        return 1.0

    # Extract nouns(NN), verbs(VB) and adjective(JJ), and convert them to their noun forms
    node1_POS_tag_list = pos_tag(word_tokenize(node1["label"]))
    node2_POS_tag_list = pos_tag(word_tokenize(node2["label"]))
    node1_word_list = convertTagListToNoun(node1_POS_tag_list)
    node2_word_list = convertTagListToNoun(node2_POS_tag_list)

    # Convert the nouns and verbs to their original forms
    node1_word_set = [lm.lemmatize(w) for w in node1_word_list]
    node2_word_set = [lm.lemmatize(w) for w in node2_word_list]
    print(node1_word_set, node2_word_set)

    # Find the intersection of word sets
    intersection = wordSetIntersection(node1_word_set, node2_word_set)
    print("Intersection", intersection)
    for word in intersection:
        try:
            score += term_weight[word]
        except Exception as e:
            print(e)
            score += 3.0    # add 3.0 for a term that is not in the term_weight. we add high score because being not
                            # in the term_weight means the term is not frequently used by others.
    
    # If one wordset is the subset of the other, conclude the labels are the same
    if checkIfWordSetIsSubset(node1_word_set, intersection):
        return 1.0
    if checkIfWordSetIsSubset(node2_word_set, intersection):
        return 1.0        

    # Find the maximum score possible for normalization
    max_score = 0
    for word in node1_word_set:
        try:
            max_score += term_weight[word]
        except Exception as e:
            max_score += 3.0
    for word in node2_word_set:
        try:
            max_score += term_weight[word]
        except Exception as e:
            max_score += 3.0
    return score/max_score

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