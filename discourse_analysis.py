import json 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import matplotlib.dates as mdates 
from tabulate import tabulate

import math

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


# ----------------------------- Load output json --------------------------


# credResult_Maker.json
with open('credResult_Maker_09142020.json') as f: 
     cred = json.load(f) 


# -------------------------- Set dates time-filtering ------------------------

# start_date = '2018/11/10 18:56:36'
start_date = '2020/09/07 00:00:00'
end_date = '2020/09/14 00:00:00'


start_datetime = datetime.datetime.strptime(start_date, '%Y/%m/%d %H:%M:%S')
end_datetime = datetime.datetime.strptime(end_date, '%Y/%m/%d %H:%M:%S')

num_nodes = len(cred[1]['credData']['nodeSummaries']) 
nodes = []

for i in range(num_nodes):

	# if (cred[1]['weightedGraph'][1]['graphJSON'][1]['sortedNodeAddresses'][i][1] == 'discourse'): 
	node = {}
	node['address'] = cred[1]['weightedGraph'][1]['graphJSON'][1]['sortedNodeAddresses'][i]
	node['cred'] = cred[1]['credData']['nodeSummaries'][i]['cred']
	if cred[1]['credData']['nodeOverTime'][i] is None: 
		node ['credOverTime'] = []
	else:
		node ['credOverTime'] = cred[1]['credData']['nodeOverTime'][i]['cred']  

	node['description'] = cred[1]['weightedGraph'][1]['graphJSON'][1]['nodes'][i]['description'] 
	node['timestamp'] = cred[1]['weightedGraph'][1]['graphJSON'][1]['nodes'][i]['timestampMs'] 
	node['user'] = ''

	if (node['address'][2] == 'IDENTITY'):
		node['user'] = cred[1]['weightedGraph'][1]['graphJSON'][1]['nodes'][i]['description']
	
	nodes.append(node)



# --------- ----------------- filter nodes by type --------------------------


nodes_filt = [ node for node in nodes if (node['address'][2]== 'post') ]
# nodes_filt = [ node for node in cred[1]["orderedNodes"] if (node['address'][2] == 'topic' )] # Filter by topic
# nodes_filt = [ node for node in cred[1]["orderedNodes"] if (node['address'][2] == 'topic' or node['address'][2]== 'post') ] # Filter by topic AND post
# nodes_filt = cred[1]["orderedNodes"]  # No filter (pass through..)



# --------------------------- filter nodes by dateTime --------------------------

nodes_time_filt = [ node for node in nodes_filt if (datetime.datetime.fromtimestamp(node['timestamp']/1000 ) >= \
		start_datetime and datetime.datetime.fromtimestamp(node['timestamp']/1000 ) <= end_datetime) ]


# --------------------- sort nodes by cred (created LAST interval) ------------

nodes_sorted3 = sorted(nodes_time_filt, key=lambda e: e['cred'], reverse=True)

table_row_contrib = []	

# pring top 10 cred 
for i in range(10):

	table_row_contrib.append([truncate(nodes_sorted3[i]['cred'],1), nodes_sorted3[i]['description'],'user'])
	print(nodes_sorted3[i]['description'])
	print("cred: " + str(truncate(nodes_sorted3[i]['cred'],1)))


# Print markdown table showing top contributions ranked by Cred
print(tabulate(table_row_contrib, ["Cred", "Contribution", "Author"], tablefmt="github")) 




# ---------------- sort by Cred earned in specified time interval (contribution created any time) --------------------


nodes_filt = [ node for node in nodes if (node['address'][2] == 'IDENTITY' )]

num_intervals = len(nodes[0]['credOverTime'])   
intervals = cred[1]['credData']['intervalEnds']#[-span:-1]
interval = num_intervals - 1  

days_l = 5  #
nodes_sorted4 = sorted(nodes_filt, key=lambda e: e['credOverTime'][interval-1]*(days_l/7) + e['credOverTime'][interval]*((7-days_l)/7) , reverse=True)


table_row_user = []

# Calculating top 10 Cred contributions
for i in range(10):

	cred_node = truncate(nodes_sorted4[i]['credOverTime'][interval-1]*(days_l/7) + nodes_sorted4[i]['credOverTime'][interval]*((7-days_l)/7),1)

	table_row_user.append([cred_node, nodes_sorted4[i]['description']])


# Print markdown table showing Cred by contributor
print(tabulate(table_row_user, ["Cred", "Contributor"], tablefmt="github")) 



# ------------------------- Plot top users Cred over time --------------------

# filter user nodes 
nodes_filt = [ node for node in nodes if (node['address'][2] == 'IDENTITY') ]
span = 8	
num_display = 10

nodes_sorted5 = sorted(nodes_filt, key=lambda e: sum(e['credOverTime'][-span:-1]), reverse=True)

top_nodes = nodes_sorted5[:num_display]


intervals = cred[1]['credData']['intervalEnds'][-span:-1]
EndDateTime = []						# Get datetime of intervals (end)
for i in range(len(intervals)):
	EndDateTime.append(datetime.datetime.fromtimestamp(intervals[i]/1000 )) 

for i in range(num_display):

	# plt.plot(EndDateTime,top_nodes[i]['credOverTime'][-span:], label=top_nodes[i]['address'][4])
	plt.plot(EndDateTime,top_nodes[i]['credOverTime'][-span:-1], label=top_nodes[i]['description'])


plt.xlabel('date')
plt.ylabel('Cred')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator())

plt.gcf().autofmt_xdate()
plt.legend()
plt.show()


