import random

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
for run in rows: 
    run_id = runs.insert(run)
    print run_id

for r in runs.find(): 
    print r

