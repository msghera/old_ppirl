from node import node
import numpy as np
from settings import settings
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import pairwise_distances
from math import log, log2, ceil
from scipy.cluster.hierarchy import dendrogram, linkage  
from matplotlib import pyplot as plt


class hierarchical_clustering:
	
	def __init__(self, _clsluter):
		self.node_lst = _clsluter
		self._prio_dict = settings().data['priority_ratio'][0]
		self.thresehold = settings().data['thresehold']
		cluster_number = np.arange(len(self.node_lst)).reshape(-1, 1)
		self.mat = pairwise_distances(cluster_number, cluster_number, metric=self.di_sim_metric)
		
	def __str__(self) : 
		return str(self.node_lst)

	def __repr__(self):		
		return str(self)

	def di_sim_metric(self, x, y):
		return self.node_lst[int(x[0])].disimilarity( self.node_lst[int(y[0])], self._prio_dict, self.thresehold)
		#return int(edist.eval(data[int(x[0])], data[int(y[0])]))

	def corelation(self, labels) :
		intra_cluster_disim , inter_cluster_sim = 0, 0
		for i in range(len(self.mat)):
			for j in range(len(self.mat)) : 
				if labels[i] == labels[j] : intra_cluster_disim += self.mat[i][j]
				else : inter_cluster_sim += (1-self.mat[i][j])
		return intra_cluster_disim + inter_cluster_sim

	def find_optimal_clustering (self) :
		minimum_corelation, number = 2**100, -1
		print('Total iteration required nearly: ' + str(ceil(log(len(self.mat), 1.5))))
		l, r, count = 1, len(self.mat), 1
		while l<r : 
			print('Iteration no #', count)
			mid1 = (l*2+r)//3
			mid2 = (l+2*r)//3;
			labels1 = self.n_clusterify(mid1)
			labels2 = self.n_clusterify(mid2)
			temp_corelation1 = self.corelation(labels1)
			temp_corelation2 = self.corelation(labels2)
			if temp_corelation1 < temp_corelation2 : r = mid2-1
			else : l = mid1 + 1
			count+=1
		return l

	def n_clusterify(self, no_of_cluster):
		agg = AgglomerativeClustering(n_clusters=no_of_cluster, affinity='precomputed',linkage='average')
		labels = agg.fit_predict(self.mat)
		return labels

	def classify(self):
		number_of_optimal_cluster = self.find_optimal_clustering()
		final_labels = self.n_clusterify(number_of_optimal_cluster)
		return final_labels