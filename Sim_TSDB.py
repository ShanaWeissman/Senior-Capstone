import argparse 
import subprocess
import psycopg2
import csv
import os
from datetime import datetime



parser = argparse.ArgumentParser()
parser.add_argument("file", type=str)
parser.add_argument("db_name", type=str)
parser.add_argument("csv_tm_header", type=str)
args = parser.parse_args()
file = args.file
db_name = args.db_name
tm_header = args.csv_tm_header
if not file.endswith(".csv"):
	raise ValueError("file must be csv file")
'''if os.path.isfile(file):
	print("file exists")'''
	
def database_setup(db_name):
	subprocess.call(["createdb", db_name])
				# Connect to Database
	conn_string = "host='hopper.cluster.earlham.edu' dbname='" + db_name + "' user='nanners'"
	conn = psycopg2.connect(conn_string)
	cur = conn.cursor()
				# Create Tables
	create_timestamp_table_string = "CREATE TABLE " + db_name + "_timestamp(timestamp TEXT)"
	cur.execute(create_timestamp_table_string)
	create_xtree_results_tb_string = "CREATE TABLE " + db_name + "_xtree_results(query_id INTEGER PRIMARY KEY, time INTERVAL, query TEXT)"
	cur.execute(create_xtree_results_tb_string)
	create_inverted_results_tb_string = "CREATE TABLE " + db_name + "_inverted_results(query_id INTEGER PRIMARY KEY, time INTERVAL, query TEXT)"
	cur.execute(create_inverted_results_tb_string)
				# Query table
	cur.execute("CREATE TABLE query (query_id INTEGER PRIMARY KEY, query TEXT)")
	conn.commit()
	return(conn, cur)
conn, cur = database_setup(db_name)
def all_broadcast_ingest_data(file, tm_header, conn, cur):
	lines = []
	with open(file) as f:
		lines = f.readlines()
	header = lines[0].split(",")
	clean_header = []
	for i in header:
		clean_header.append(i.rstrip())
	ind = clean_header.index(tm_header) # this is the ind number in each row that has the timestamp
	time_obj = ""
	for line in lines:
		
		try:
			if len(line.split(",")) == 5:
				time_obj = datetime.strptime(line.split(",")[ind].rstrip(), "%Y-%m-%d %H:%M:%S.%f")
				insert_str="INSERT INTO " + db_name + "_timestamp (timestamp) values ('" + str(time_obj) + "')"
				cur.execute(insert_str)
				print(insert_str)
		except:
			pass

		

		
	conn.commit()
		
all_broadcast_ingest_data(file, tm_header, conn, cur)


