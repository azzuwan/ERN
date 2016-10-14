#!/usr/bin/env python
import rethinkdb as rdb
import time
import pprint

rdb.connect(host='192.168.1.214', port=28015, db='ERN').repl()

# rdb.table("nodes").insert([
# 	{"node_id" : "ern1", 
# 	"lat" : "2.355543333", 
# 	"long": "102.102116667", 
# 	"timestamp": 
# 	time.time() }
# 	]).run()

time.sleep(3)
cursor = rdb.table("nodes").filter(lambda node: node["node_id"].match("ern1")).run()
data = list(cursor)
if not data:
	print("record is empty")
else:
	for d in data:
		print d