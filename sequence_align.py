def align(seq1, seq2, scorefunc, nodes, nodes_group):
	dp = [[0 for x in range(len(seq2))] for y in range(len(seq1))]
	seq = [[0 for x in range(len(seq2))] for y in range(len(seq1))]

	for i in range(len(seq1)):
		for j in range(len(seq2)):
			dp_i_1_j_1 = 0
			dp_i_j_1 = 0
			dp_i_1_j = 0
			if(i > 0):
				dp_i_1_j = dp[i-1][j]
			if(j > 0):
				dp_i_j_1 = dp[i][j-1]
			if(i > 0 and j > 0):
				dp_i_1_j_1 = dp[i-1][j-1]

			cand1 = dp_i_1_j_1 + scorefunc(seq1[i], seq2[j], nodes, nodes_group)
			cand2 = dp_i_1_j + 0
			cand3 = dp_i_j_1 + 0
			dp[i][j] = max(cand1, cand2, cand3)
			if(dp[i][j] == cand1):
				seq[i][j] = "1"
			elif(dp[i][j] == cand2):
				seq[i][j] = "2"
			else:
				seq[i][j] = "3"


	i = len(seq1)-1
	j = len(seq2)-1
	seq1_txt = []
	seq2_txt = []
	while(i >= 0 and j >= 0):
		if(seq[i][j] == "1"):
			seq1_txt.insert(0, str(seq1[i]))
			seq2_txt.insert(0, str(seq2[j]))
			i -= 1
			j -= 1
		elif(seq[i][j] == "2"):
			seq1_txt.insert(0, str(seq1[i]))
			seq2_txt.insert(0, "_")
			i -= 1
		elif(seq[i][j] == "3"):
			seq1_txt.insert(0, "_")
			seq2_txt.insert(0, str(seq2[j]))
			j -= 1
		else:
			print("Exception", seq[i][j])

	while(i >= 0):
		seq1_txt.insert(0, str(seq1[i]))
		seq2_txt.insert(0, "_")
		i -= 1
	while(j >= 0):
		seq1_txt.insert(0, "_")
		seq2_txt.insert(0, str(seq2[j]))
		j -= 1

	return [seq1_txt, seq2_txt, dp[len(seq1)-1][len(seq2)-1]]