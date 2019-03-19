from node import node

class cluster :
	
	def __init__ (self) :
		self.node_lst = []
		self.dis_mat = []
		self.intra_cluster_correlation = 0.0
		self.not_committed = 0

	def __len__(self):
		return len(self.node_lst)

	def push(self, _node):
		node_lst.append(_node)
		self.not_committed += 1

	def pop(self) :
		return node_lst.pop()		

	def __str__(self) :
		return str(self.node_lst)

	def commit(self):
		for i in range(self.not_committed):
			print(i)
		

if __name__ == '__main__':
	print('Here')

