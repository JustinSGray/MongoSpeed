import random
import time 

from pymongo import MongoClient
 


N_ROWS = 10 
N_VARS = 100

#generate the bs data
rows = []
for i in xrange(N_ROWS): 
    row = {}
    row['name'] = "run %d"%i
    for j in xrange(N_VARS): 
        row['var_%d'] = random.random()
    rows.append(row)


#connect to the database
client = MongoClient()
db = client.test_database


runs = db.runs
db.runs.remove()

start_time = time.time()

for run in rows: 
    run_id = runs.insert(run)

print "time per insert: ", (time.time() - start_time)/N_ROWS




