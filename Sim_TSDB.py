import argparse 
import subprocess
import psycopg2
import csv
import os
from datetime import datetime, timedelta
import random
import invertedindex



parser = argparse.ArgumentParser()
parser.add_argument("file", type=str)
parser.add_argument("db_name", type=str)
parser.add_argument("csv_tm_header", type=str)
parser.add_argument("time_format", type=str)
args = parser.parse_args()
file = args.file
db_name = args.db_name
tm_header = args.csv_tm_header
time_format=args.time_format.replace(",", " ")


if not file.endswith(".csv"):
	raise ValueError("file must be csv file")

	
def create_conn(db_name):
	try:		#Necessary for if the DB already exists with Data in it
		subprocess.call(["createdb", db_name]) 
	except:
		pass 
				# Connect to Database
	conn_string = "host='hopper.cluster.earlham.edu' dbname='" + db_name + "' user='nanners'"
	conn = psycopg2.connect(conn_string)
	cur = conn.cursor()
	return(conn, cur)
		
	
				# Create Tables
def database_set_up(conn, cur):
	create_timestamp_table_string = "CREATE TABLE " + db_name + "_timestamp(timestamp TIMESTAMP)"
	cur.execute(create_timestamp_table_string)
	create_xtree_results_tb_string = "CREATE TABLE " + db_name + "_xtree_results(query_id INTEGER PRIMARY KEY, time INTERVAL, query TEXT)"
	cur.execute(create_xtree_results_tb_string)
	create_inverted_results_tb_string = "CREATE TABLE " + db_name + "_inverted_results(query_id INTEGER PRIMARY KEY, time INTERVAL, query TEXT)"
	cur.execute(create_inverted_results_tb_string)
				# Query table
	cur.execute("CREATE TABLE query (query_id INTEGER PRIMARY KEY, query TEXT)")
	conn.commit()
	

def ingest_data(file, tm_header, conn, cur, time_format):

	lines = []
	with open(file) as f:
		lines = f.readlines()
	header = lines[0].split(",")
	clean_header = []
	for i in header:
		clean_header.append(i.rstrip())
	ind = clean_header.index(tm_header) # this is the ind number in each row that has the timestamp
	print("index of time:  ", ind, "len of header: ", len(header))
	time_obj = ""
	for line in lines:
		try:
			if len(line.split(",")) == len(header):
				if time_format == "epoch":
					time_convert_format = "%Y-%m-%d %H:%M:%S"
					epoch_time = datetime.fromtimestamp(float(line.split(",")[ind].rstrip()))
					time_obj = epoch_time.strftime(time_convert_format)
					
					print(time_obj)
				else:
					time_obj = datetime.strptime(line.split(",")[ind].rstrip(), time_format)
				insert_str="INSERT INTO " + db_name + "_timestamp (timestamp) values (TIMESTAMP '" + str(time_obj) + "')"  
				print(insert_str)
				cur.execute(insert_str)
				
		except:
			pass

	conn.commit()



def find_bounds(cur, db_name):
	cur.execute("select MIN(timestamp) from " + db_name + "_timestamp") 
	min_time = cur.fetchone()[0]
	cur.execute("select MAX(timestamp) from " + db_name + "_timestamp") 
	max_time = cur.fetchone()[0]
	return(min_time, max_time)
	
	
def get_first_val(duration, min_time):
	added_seconds = random.randint(0, duration + 1)
	return(min_time + timedelta(seconds=added_seconds))
	
def check_values_diff(time_one, time_two):
	if time_one == time_two:
		return(True)
	else:
		return(False)
	
def get_second_val(duration, min_time, time_one):
	added_seconds = random.randint(0, duration + 1)
	time_two = min_time + timedelta(seconds=added_seconds)
	while check_values_diff(time_one, time_two):
		added_seconds = random.randint(0, duration + 1)
		time_two = min_time + timedelta(seconds=added_seconds)	
	return(time_two)	
		
def return_larger_timestamp(time_one, time_two):
	if time_one > time_two:
		return(time_one, time_two)
	else:
		return(time_two, time_one)
		
def equality_query(IndexStructure, target_timestamp):
	time_a = datetime.now()
	IndexStructure.point_search(target_timestamp)
	time_b = datetime.now()
	result = time_b - time_a
	return(result)
	
def bounded_query(IndexStructure, left, right):
	time_a = datetime.now()
	IndexStructure.bounded_range_search(left, right)
	time_b = datetime.now()
	result = time_b - time_a
	return(result)
	
def unbounded_query(IndexStructure, left, right):
	time_a = datetime.now()
	IndexStructure.unbounded_range_search(left, right)
	time_b = datetime.now()
	result = time_b - time_a
	return(result)

def remove_value(IndexStructure, target):
	time_a = datetime.now()
	IndexStructure.remove_value(target)
	time_b = datetime.now()
	result = time_b - time_a
	return(result)

def insert_value(IndexStructure, target):
	time_a = datetime.now()
	IndexStructure.insert_value(target)
	time_b = datetime.now()
	result = time_b - time_a
	return(result)	
def write_result(conn, cur, db_name, querytype, target, result, which_structure, id):
	#fse_inverted_results
	if type(target) == list:
		query = querytype
		for i in target:
			query = query + " " + str(i)
	else:
		query = querytype + " " + str(target)
	
	cur.execute("INSERT INTO " + db_name.lower() + "_" + which_structure + "_results (query_id, time, query) values (%s, %s, %s)", (id, str(result), query))
	conn.commit()
	
def querie_generator(n, conn, cur, db_name, IndexStructure, which_structure):
	min_timestamp, max_timestamp = find_bounds(cur, db_name)
	duration = (max_timestamp - min_timestamp).seconds
	query_id = 0
	
	for i in range(n):
		timestamp_one = get_first_val(duration, min_timestamp)
		timestamp_two = get_second_val(duration, min_timestamp, timestamp_one)
		larger_timestamp, smaller_timestamp = return_larger_timestamp(timestamp_one, timestamp_two)
		
		#equality query:
		result = equality_query(IndexStructure, smaller_timestamp)
		write_result(conn, cur, db_name, "equality", smaller_timestamp, result, which_structure, query_id)
		print("equality query, id: ", query_id, "size: ", IndexStructure.get_size())
		query_id = query_id + 1
		
		#bounded query
		result = bounded_query(IndexStructure, smaller_timestamp, larger_timestamp)
		write_result(conn, cur, db_name, "bounded", [smaller_timestamp, larger_timestamp], result, which_structure, query_id)
		print("bounded query, id: ", query_id, "size: ", IndexStructure.get_size())
		query_id = query_id + 1
		
		#unbounded_query
		result = unbounded_query(IndexStructure, smaller_timestamp, larger_timestamp)
		write_result(conn, cur, db_name, "unbounded", [smaller_timestamp, larger_timestamp], result, which_structure, query_id)
		print("unbounded query, id: ", query_id, "size: ", IndexStructure.get_size())
		query_id = query_id + 1
		
		#remove value
		result = remove_value(IndexStructure, smaller_timestamp)
		write_result(conn, cur, db_name, "remove", smaller_timestamp, result, which_structure, query_id)
		print("remove, id: ", query_id, "size: ", IndexStructure.get_size())
		query_id = query_id + 1
		
		#insert value
		result = insert_value(IndexStructure, smaller_timestamp)
		write_result(conn, cur, db_name, "insert", smaller_timestamp, result, which_structure, query_id)
		print("insert, id: ", query_id, "size: ", IndexStructure.get_size())
		query_id = query_id + 1
		
				
		'''
		if i % 100 == 0:
			print("on query: ", i)
		'''
		



		
def invertedindex_runthrough(conn, cur, db_name):
	#Create Index
	IndexStructure = invertedindex.inverted_index()
	#get values from psql
	cur.execute("select timestamp from " + db_name + "_timestamp")
	timestamps = cur.fetchall()
	print("number of timestamps: ", len(timestamps))
	#insert each value
	count = 0
	for timestamp in timestamps:
		IndexStructure.insert_value(timestamp[0])
		count += 1
		if count%100 == 0:
			print("merge sort: ", count)
	#IndexStructure.show_index()
	print("merge sort done")
	
	#query generator
	querie_generator(500, conn, cur, db_name, IndexStructure, "inverted")
	#delete index



def main():
	conn, cur = create_conn(db_name)
	#database_set_up(conn, cur)
	#ingest_data(file, tm_header, conn, cur, time_format)
	invertedindex_runthrough(conn, cur, db_name)
	#xtree_runthrough()


main()
#querie_generator(5, conn, cur, db_name)




