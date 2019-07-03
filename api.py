from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_restful import reqparse
import pyrebase
from graph import Graph
from sequence_align import align
import textdistance
import json

# from gensim.models.keyedvectors import KeyedVectors
# model = KeyedVectors.load_word2vec_format("./models/glove_vectors.txt", binary=False)

with open('db-config.json') as db_config_file:    
    config = json.load(db_config_file)

firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)
api = Api(app)

class Similarity(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('w1', type=str)
            parser.add_argument('w2', type=str)
            args = parser.parse_args()

            w1 = args['w1']
            w2 = args['w2']
            # sim = str(model.similarity(w1, w2))
            sim = "1"
            return {'w1': w1, 'w2': w2, 'similarity': sim}
        except Exception as e:
            return {'error': str(e)}

class Sequence_align(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)
            topic = data["topic"]
            problem_num = data["problem_num"]
            in_seq = data["in_seq"]
            threshold = int(data["threshold"])

            in_nodes = in_seq["nodes"]
            in_edges = in_seq["edges"]

            solution_graph = db.child(topic+"/problems/"+problem_num+"/complete_new").get().val()
            G = Graph(solution_graph)

            return sequence_align(in_nodes, in_edges, G, threshold)

        except Exception as e:
            return {'error': str(e)}

class Sequence_align_min(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)
            topic = data["topic"]
            problem_num = data["problem_num"]
            in_seq = data["in_seq"]
            threshold = int(data["threshold"])
            target = float(data["target"])

            in_nodes = in_seq["nodes"]
            in_edges = in_seq["edges"] if "edges" in in_seq else []

            solution_graph = db.child(topic+"/problems/"+problem_num+"/complete_new").get().val()
            G = Graph(solution_graph)

            return sequence_align_min(in_nodes, in_edges, G, threshold, target)

        except Exception as e:
            return {'error': str(e)}

class Merge_sequence(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)
            topic = data["topic"]
            problem_num = data["problem_num"]
            sequences = db.child(topic+"/problems/"+problem_num+"/sequences").get().val()

            cnt = 0
            G = Graph({"max_index": -1, "nodes": [], "edges": [], "heads": [], "n": cnt})

            for key in sequences:
                nodes = sequences[key]["nodes"]
                if("edges" in sequences[key]):
                    edges = sequences[key]["edges"]
                else:
                    edges = []

                if(cnt == 0):
                    for node in nodes:
                        G.add_node(node, (nodes.index(node)) == 0)
                    for edge in edges:
                        G.add_edge([ int(edge[0]), int(edge[1]) ])
                else:
                    merge_sequence(nodes, edges, G)
                cnt += 1

            G.n = cnt
            G.print_nodes()

            return G.get_snapshot()

        except Exception as e:
            return {'error': str(e)}

def merge_sequence(nodes, edges, G):
    result = sequence_align(nodes, edges, G, 1)
    max_seq1 = result[1]
    max_seq2 = result[2]

    print(result)

    translation = {}
    for i in range(len(max_seq1)):
        if(max_seq1[i] != "_" and max_seq2[i] != "_"):
            node = idx_to_node([max_seq1[i]], nodes)[0]
            if(int(max_seq1[i]) == int(nodes[0]["index"])):
                G.heads.append(int(max_seq2[i]))
                G.heads = list(set(G.heads));
            node_group_node = G.get_node(max_seq2[i])
            node_group_node["nodes"].append(node)
            translation[max_seq1[i]] = max_seq2[i]
        elif(max_seq1[i] == "_"):
            continue
        else:
            node = idx_to_node([max_seq1[i]], nodes)[0]
            new_idx = G.add_node(node, int(max_seq1[i]) == int(nodes[0]["index"]))
            translation[max_seq1[i]] = str(new_idx)
    for edge in edges:
        G.add_edge([ int(translation[str(edge[0])]), int(translation[str(edge[1])]) ])
    G.n += 1

def sequence_align_min(nodes, edgs, G, threshold, min_similarity=2.0):
    node_group_idx = G.get_idxs()
    node_group_head = G.get_heads()
    nodes_idx = node_to_idx(nodes)
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
            match = align(nodes_idx, subsequence, scoreFunc, nodes, G.get_nodes())
            if(abs(match[2] - min_similarity) < min_diff):
                min_diff = abs(match[2] - min_similarity)
                min_seq1 = match[0]
                min_seq2 = match[1]
    return [min_diff, min_seq1, min_seq2]

def sequence_align(nodes, edges, G, threshold):
    node_group_idx = G.get_idxs()
    node_group_head = G.get_heads()
    nodes_idx = node_to_idx(nodes)
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
            match = align(nodes_idx, subsequence, scoreFunc, nodes, G.get_nodes())
            if(match[2] > max_val):
                max_val = match[2]
                max_seq1 = match[0]
                max_seq2 = match[1]
    return [max_val, max_seq1, max_seq2]

threshold = 0.2
def scoreFunc(node_idx, node_group_idx, nodes, node_group):
    chosen_nodes = idx_to_node([node_idx], nodes)[0]
    chosen_node_group = idx_to_node([node_group_idx], node_group)[0]["nodes"]
    similarity = node_similarity(chosen_nodes, chosen_node_group)
    if(similarity > threshold):
        return similarity
    else:
        return -1 * similarity

def node_similarity(node, nodes):
    score = 0
    for each_node in nodes:
        score += pow(step_similarity(each_node, node), 2)
    score /= len(nodes)
    return score

def step_similarity(node1, node2):
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

def node_to_idx(node_group):
    ret = []
    for node in node_group:
        ret.append(node["index"])
    return ret

def idx_to_node(lst, nodes):
    ret = [];
    for idx in lst:
        for node in nodes:
            if(int(node["index"]) == int(idx)):
                ret.append(node)
    return ret

api.add_resource(Similarity, '/w2v_similarity')
api.add_resource(Sequence_align, '/seq_align')
api.add_resource(Sequence_align_min, '/seq_align_min')
api.add_resource(Merge_sequence, '/merge_sequence')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001, debug=True)
