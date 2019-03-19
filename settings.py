import json
import sys
from pathlib import Path

class settings :

	def __init__ (self, filepath = 'settings.set'): 

		with open(filepath) as f:
			self.data = json.load(f)
		try : 
			ratio_sum = 0.0
			for i in self.data['priority_ratio'][0] :
				self.data['priority_ratio'][0][i] = float(self.data['priority_ratio'][0][i])
				ratio_sum += self.data['priority_ratio'][0][i]
			if ratio_sum != 1.00 : raise Exception ('Sum of priority is not 1')

		except Exception as error_msg :
			print('Error Occured : ' + str(error_msg))

	def __str__(self):
		return str(self.data)

	def __repr__(self):
		return str(self)

if __name__ == '__main__' :
	new_set = settings()