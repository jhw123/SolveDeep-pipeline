from graph import Graph
from sequence_align import align
import textdistance
from gensim.models.keyedvectors import KeyedVectors

print("loading a word2vec model...")
model = KeyedVectors.load_word2vec_format("./models/glove_vectors.txt", binary=False)
print("glove_vectors model is loaded successfully")

def addSequenceToGraph(nodes, edges, G):
    result = findMostSimilarGraphSequence(nodes, edges, G, 1)
    max_seq1 = result[1]
    max_seq2 = result[2]

    translation = {}
    for i in range(len(max_seq1)):
        if(max_seq1[i] != "_" and max_seq2[i] != "_"):
            node = getNodesForIndexes([max_seq1[i]], nodes)[0]
            if(int(max_seq1[i]) == int(nodes[0]["index"])):
                G.heads.append(int(max_seq2[i]))
                G.heads = list(set(G.heads));
            node_group_node = G.get_node(max_seq2[i])
            node_group_node["nodes"].append(node)
            translation[max_seq1[i]] = max_seq2[i]
        elif(max_seq1[i] == "_"):
            continue
        else:
            node = getNodesForIndexes([max_seq1[i]], nodes)[0]
            new_idx = G.add_node(node, int(max_seq1[i]) == int(nodes[0]["index"]))
            translation[max_seq1[i]] = str(new_idx)
    for edge in edges:
        G.add_edge([ int(translation[str(edge[0])]), int(translation[str(edge[1])]) ])
    G.n += 1

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
            match = align(nodes_idx, subsequence, globalAlignmentScoreFunc, nodes, G.get_nodes())
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
            match = align(nodes_idx, subsequence, globalAlignmentScoreFunc, nodes, G.get_nodes())
            if(match[2] > max_val):
                max_val = match[2]
                max_seq1 = match[0]
                max_seq2 = match[1]
    return [max_val, max_seq1, max_seq2]

threshold = 0.2
def globalAlignmentScoreFunc(node_idx, node_group_idx, nodes, node_group):
    chosen_nodes = getNodesForIndexes([node_idx], nodes)[0]
    chosen_node_group = getNodesForIndexes([node_group_idx], node_group)[0]["nodes"]
    similarity = node_similarity(chosen_nodes, chosen_node_group)
    if(similarity > threshold):
        return similarity
    else:
        return -1 * similarity

def node_similarity(node, nodes):
    score = 0
    for each_node in nodes:
        score += pow(computeSubgoalLabelSimilarity(each_node, node), 2)
    score /= len(nodes)
    return score

def computeSubgoalLabelSimilarity(node1, node2):
    node1step = '|'.join(node1["steps"]).lower()
    node2step = '|'.join(node2["steps"]).lower()
    score = 0

    score += textdistance.hamming.normalized_similarity(node1["noun"].lower(), node2["noun"].lower())/3
    try:
         score += model.similarity(node1["verb"].lower(), node2["verb"].lower())*0.75
    except Exception as e:
         print(e)

    if(node1["noun"].lower() == node2["noun"].lower() and node1["verb"].lower() == node2["verb"].lower()):
        score += 1
    score += textdistance.hamming.normalized_similarity(node1step, node2step)/3
    return score

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