from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_restful import reqparse
import pyrebase
import json
from graphAlignOperation import *

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
            sim = str(model.similarity(w1, w2))
            # sim = "1"
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

            return findMostSimilarGraphSequence(in_nodes, in_edges, G, threshold)

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

            return findTargetSimilarityGraphSequence(in_nodes, in_edges, G, threshold, target)

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
            G = Graph({"max_index": -1, "nodes": [], "edges": [], "heads": [], "tails": [], "n": cnt})

            for key in sorted(sequences.keys()):
                nodes = sequences[key]["nodes"]
                if("edges" in sequences[key]):
                    edges = sequences[key]["edges"]
                else:
                    edges = []

                if(cnt == 0):
                    for node in nodes:
                        new_idx = G.add_node(node)
                        if (nodes.index(node)) == 0:
                            G.add_head(new_idx)
                        elif (nodes.index(node)) == len(nodes):
                            G.add_tail(new_idx)
                    for edge in edges:
                        G.add_edge([ int(edge[0]), int(edge[1]) ])
                else:
                    alignment = findMostSimilarGraphSequence(nodes, edges, G, 1)
                    seq_alignment = alignment[1]
                    graph_alignment = alignment[2]
                    G.addSequenceToGraph(nodes, edges, seq_alignment, graph_alignment)
                cnt += 1

            G.n = cnt
            G.print_nodes()

            return G.get_snapshot()

        except Exception as e:
            return {'error': str(e)}

# class Word_frequency(Resource):
#     def post(self):
#         try:
#             data = request.get_json(force=True)
#             topic = data["topic"]
#             problem_num = data["problem_num"]
#             sequences = db.child(topic+"/problems/"+problem_num+"/sequences").get().val()

#             term_weight = getSubgoalTermWeight(sequences)

#             with open('term_weight.json', 'w') as f:
#                 json.dump(term-weight, f)

#             return term_weight

#         except Exception as e:
#             return {'error': str(e)}

class Compare_subgoals(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)
            return computeSubgoalLabelSimilarity({"label": data["label1"]}, {"label": data["label2"]})
        except Exception as e:
            return {'error': str(e)}

api.add_resource(Similarity, '/w2v_similarity')
api.add_resource(Sequence_align, '/seq_align')
api.add_resource(Sequence_align_min, '/seq_align_min')
api.add_resource(Merge_sequence, '/merge_sequence')
api.add_resource(Compare_subgoals, '/compare_subgoals')
# api.add_resource(Word_frequency, '/word_frequency')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001, debug=True)
