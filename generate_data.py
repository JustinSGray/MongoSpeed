import random
import time 

from pymongo import MongoClient

import numpy as np

from matplotlib import pylab as p


#connect to the database
client = MongoClient()
db = client.test_database
runs = db.runs
 
N_ROWS = int(1e3)
N_VARS = int(1e3)

sizes = [1000,10000,50000,100000]
#sizes = [10,20,30]

insert_times = []
query_times = []



#for N_ROWS in sizes:
for N_ROWS in [100]: 
    i_times = []
    q_times = []
    for N_VARS in sizes: 
        print "testing %d data rows with %d variables in each"%(N_ROWS, N_VARS)
        #generate the bs data
        rows = []
        for i in xrange(N_ROWS): 
            row = {}
            row['name'] = "run %d"%i
            for j in xrange(N_VARS): 
                row['var_%d'%j] = random.random()
            rows.append(row)
        
        db.runs.remove()

        start_time = time.time()

        for run in rows: 
            run_id = runs.insert(run)

        t_per_insert = (time.time() - start_time)/float(N_ROWS)


        start_time = time.time()
        for j in xrange(10): 
            var_name = 'var_%d'%j
            runs.ensure_index(var_name) 
            #NOTE: building these indecies can be expensive, 
            # so you would not want to do that for every variable... 
            # indecies also affect write performance
            # but you need an index for any large variable sets inorder to do the sort, or MongoDB errors
            [r["name"] for r in runs.find().sort(var_name)[:100]]

        t_per_query = (time.time() - start_time)/float(N_VARS)

        i_times.append(t_per_insert)
        q_times.append(t_per_query)

    insert_times.append(i_times)
    query_times.append(q_times)


f = open('db_times.out','w')

print >> f, "insert_times=", insert_times
print >> f, "query_times=", query_times

for n_data_rows,row in zip(sizes, insert_times): 
    p.plot(sizes, row, label="%d rows"%n_data_rows)


p.title("Sec. insert vs #of variables")
p.xlabel('# of variables')
p.ylabel('seconds per insert')
p.legend(loc="best")

p.figure()
for n_data_rows,row in zip(sizes, query_times): 
    p.plot(sizes, row, label="%d rows"%n_data_rows)
p.title("Sec. per sorted query vs #of variables")
p.xlabel('# of variables')
p.ylabel('seconds per sorted query')
p.legend(loc="best")

p.show()














