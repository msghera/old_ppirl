from node import node
import pandas as pd
from settings import settings
from hierarchical_clustering import hierarchical_clustering as hc
from connected_component import find_connected_components as fcc
import random 
import time 

#Name,Gender,Age,Contact,Address
_setting = settings()

def get_data (_file_name, data_size = 2500):
	all_node = read_node(_file_name)
	for i in range(len(all_node), data_size) :
		temp  = random.randint(0, len(all_node)-1)
		all_node.append(all_node[temp])
	random.shuffle(all_node)
	return all_node[:data_size]

def read_node (_file_name) :
	file_df = pd.read_csv(_file_name)
	return [node(file_df['Name'].iloc[i], file_df['Gender'].iloc[i], file_df['Age'].iloc[i], file_df['Contact'].iloc[i], file_df['Address'].iloc[i], _file_name+'~' +str(i) ) for i in range(len(file_df))]	

def relabel(lst):
	mp, count = dict(), 0
	for i in lst :
		if i not in mp.keys() : 
			mp[i] = count
			count+=1
	return [mp[i] for i in lst]

def process_increment(primary_label, node_lst, increment_lst): 
	model = hc(node_lst + increment_lst) 
	cc = (fcc(model.mat, len(increment_lst), primary_label))
	_node_lst, _increment_lst,_primary_label = [], increment_lst[:], []
	for i in range(len(node_lst)):
		if cc[primary_label[i]] == True: _increment_lst.append(node_lst[i])
		else : 
			_node_lst.append(node_lst[i])
			_primary_label.append(primary_label[i])			
	model = hc(_increment_lst) 
	offset = int(1e10)
	increment_label = [i+offset for i in model.classify()]
	final_label = relabel(_primary_label + increment_label)
	return (final_label, _node_lst + increment_lst)

def eval_time (start_time , end_time):
	elapsed_time = (end_time - start_time)
	seconds=int((elapsed_time)%60)
	minutes=int((elapsed_time/60)%60)
	hours=int ((elapsed_time/(60*60))%24)
	print ("Time elapsed : %d hours, %d minutes, %d second" % (hours, minutes, seconds))

def eval_cluster(preditced_labels, actual_labels):
	print(preditced_labels, actual_labels)
	true_positive, true_negative, false_positive, false_negative = [], [], [], []
	if len(preditced_labels) != len(actual_labels) : raise Exception ("Lenght mismatch for two different labels")
	confusion_matrix_size = max([max(preditced_labels), max(actual_labels)])+1
	row_sum, col_sum, dia_sum = [0] * confusion_matrix_size, [0] * confusion_matrix_size, 0
	confusion_matrix = [[0 for __ in range (confusion_matrix_size)] for _ in range (confusion_matrix_size)]
	for i in range(confusion_matrix_size):
		for j in preditced_labels:
			confusion_matrix[i][j]+=1
	for i in range(confusion_matrix_size):
		dia_sum+=confusion_matrix[i][i]
		for j in range(confusion_matrix_size):
			row_sum[i]+=confusion_matrix[i][j]
			col_sum[j]+=confusion_matrix[i][j]
			
	for i in range(confusion_matrix_size):
		true_positive.append(confusion_matrix[i][i])
		true_negative.append(confusion_matrix_size * confusion_matrix_size - row_sum[i] + col_sum[i] - confusion_matrix[i][i])
		false_positive.append(col_sum[i] - confusion_matrix[i][i])
		false_negative.append(row_sum[i] - confusion_matrix[i][i])
	return {
		'size' : confusion_matrix_size,
		'true_positive' : true_positive,
		'true_negative' : true_negative,
		'false_positive' : false_positive,
		'false_negative' : false_negative
	}

def main(initial_size = 1000):
	node_lst = get_data('data//base.csv', 5)
	initial_node_lst = node_lst[:initial_size]
	print('Initial Clustering is starrting.')
	start_time = time.time()
	model = hc(initial_node_lst) 
	initial_label = relabel(model.classify())
	eval_time(start_time, time.time())
	print('Initial Clustering is finished.')
	print(eval_cluster(initial_label, initial_label))

if __name__ == '__main__' :
	main(5)
	