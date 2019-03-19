from jellyfish import jaro_distance as jd
from settings import settings
from  stringdist import levenshtein as lev

class node :
	def __init__(self, _name = '', _gender = '', _age = 0, _contact = '0000', _address = '000000', _id = 'id', _label = -1):
		self.name 		= str(_name)
		self.gender 	= str(_gender)
		self.age 		= str(_age)
		self.contact 	= str(_contact)
		self.address 	= str(_address)
		self.id 		= str(_id)
		self.label 		= int(_label)

	def get_label(self) :
		return self.label

	def __str__(self):		
		return str(self.id) + '~' + self.name + '~' + self.gender + '~' + str(self.age) + '~' + self.contact + '~' + self.address

	def __repr__(self):		
		return str(self)

	def sim_age(self, frst_age, scnd_age) :
		abs_dif = abs(int(frst_age) - int(scnd_age))
		return (100-abs_dif)/100

	def sim_contact(self, frst_contact, contact_contact) :
		abs_dif = lev(frst_contact , contact_contact)
		if abs_dif > 2 : return 0
		else : return 2/(2**(abs_dif+1))

	def sim_address(self, frst_address, scnd_address) :		
		if frst_address == scnd_address : return 1
		elif frst_address[0:4] == scnd_address[0:4] : return 0.5
		elif frst_address[0:2] == scnd_address[0:2] : return 0.25
		else :return 0

	def disimilarity (self, scnd, prio_dct,thresehold = 0.7) :
		similarity_sum = 0.0
		similarity_sum += (jd(self.name, scnd.name) * prio_dct['name'])
		similarity_sum += (self.sim_age(self.age, scnd.age) * prio_dct['age'])
		if self.gender == scnd.gender : similarity_sum += prio_dct['gender']
		similarity_sum += (self.sim_contact(self.contact, scnd.contact) * prio_dct['contact'])
		similarity_sum += (self.sim_address(self.address, scnd.address) * prio_dct['address'])
		if similarity_sum < thresehold : similarity_sum = 0
		return 1-similarity_sum

if __name__ == '__main__' : 
	frst = node('Mohammad Sheikh Ghazanfar' , 'Male', 23, '01917051204', '696867')
	scnd = node('Muhammad Shekh Gazanfar' , 'Male', 24, '01917051104', '691212')
	_setting = settings()
	print(frst.disimilarity(scnd, _setting.data['priority_ratio'][0]))