#MBR-->minimum bounding rectangle
#ptr-->pointer
#dir node holds 1 entry
import time
class MBR():
	def __init__(self, min_time, max_time):
		self.min_time = min_time
		self.max_time = max_time
class dir_node():
	def __init__(self, MBRs, ptr):
		self.MBRs = MBRs
		self.ptr = ptr
class data_node():
	def __init__(self, obj_id, ptr=Null):
		self.obj_id = obj_id
		self.ptr = ptr
class supernode():
	def __init__(self, obj_id, ptr):

def create_xtree(): #the root node will have an MBR containing the range of the entire data set
	root_MBR = MBR()
#def insert_dir_node(data_obj, new_dir_node):
