'''
Designed to contain important functions.
'''

vis_node, vis_cluster, cluster_labels, adj_lst = [], [], [], []

def dfs (u) :
	global vis_node, vis_cluster, adj_lst, cluster_labels
	vis_node [u] = True
	if u<len(cluster_labels) : vis_cluster[cluster_labels[u]] = True	
	for i in adj_lst[u]:
		if vis_node[i] == False : dfs(i)

def find_connected_components(mat, increment_size, labels):
	global vis_node, vis_cluster, adj_lst, cluster_labels
	size = len(mat)
	vis_node = [False] * size
	cluster_labels = labels
	vis_cluster = [False] * len(cluster_labels)
	adj_lst = [[] for _ in range(size)]
	for i in range(size) :
		for j in range(0, len(mat[i])) :
			if (i!= j and 1 - mat[i][j]) > 0.0 : adj_lst[i].append(j)
	for i in range(len(cluster_labels), size) : dfs(i)
	return vis_cluster

if __name__ == '__main__' : 
	print(similarity(1, 2))