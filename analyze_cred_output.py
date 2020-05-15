import json 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime


# --------- Load output json ---------

with open('output_maker2.json') as f: 
     cred = json.load(f) 


# --------- Set time-filtering ------------

# start_date = '2018/11/10 18:56:36'
start_date = '2020/05/03 00:00:00'
end_date = '2020/05/10 00:00:00'


start_datetime = datetime.datetime.strptime(start_date, '%Y/%m/%d %H:%M:%S')
end_datetime = datetime.datetime.strptime(end_date, '%Y/%m/%d %H:%M:%S')



# --------- Filter nodes by type ----------

nodes_filt = [ node for node in cred[1]["orderedNodes"] if (node['address'][2] == 'topic' )]
# nodes_filt = [ node for node in cred[1]["orderedNodes"] if (node['address'][2] == 'topic' or node['address'][2]== 'post') ]
# nodes_filt = [ node for node in cred[1]["orderedNodes"] if (node['address'][2] == 'user' )]



# ------------- filter nodes by dateTime --------

nodes_time_filt = [ node for node in nodes_filt if (datetime.datetime.fromtimestamp(node['timestamp']/1000 ) >= \
		start_datetime and datetime.datetime.fromtimestamp(node['timestamp']/1000 ) <= end_datetime) ]


# -------------- sort nodes by cred ------------

# sort by all-time cred
nodes_sorted2 = sorted(nodes_time_filt, key=lambda e: e['cred'], reverse=True)


# sort by cred earned in the latest interval
num_intervals = len(cred[1]["orderedNodes"][0]['credOverTime'])   
interval = num_intervals - 1  
nodes_sorted3 = sorted(nodes_time_filt, key=lambda e: e['credOverTime'][interval], reverse=True)

# pring top 10 cred 
for i in range(10):
	print(nodes_sorted3[i]['description'])
	print("cred: " + str(nodes_sorted3[i]['credOverTime'][interval]))



