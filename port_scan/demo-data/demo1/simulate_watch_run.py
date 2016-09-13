__author__ = 'dale'
from elasticsearch import Elasticsearch
import argparse
from elasticsearch import Elasticsearch
from elasticsearch_watcher import WatcherClient
import json
parser = argparse.ArgumentParser(description='Simulates running the port scan watcher over an index containing correctly structured data')
parser.add_argument('--host',help='host name')
parser.add_argument('--port',help='port')
parser.add_argument('--watch_file',help='watch file')
parser.add_argument('--mapping_file',help='mapping file')
parser.set_defaults(host='localhost',port="9200",watch_file='simulation_watch.json',mapping_file='scan_mapping.json')
args = parser.parse_args()

es = Elasticsearch([args.host+":"+args.port])

#Identifies the date range of the index
stats=es.field_stats(index="connection",params={"fields":"@timestamp"})
min_time=long(stats['indices']['_all']['fields']['@timestamp']['min_value'])
max_time=long(stats['indices']['_all']['fields']['@timestamp']['max_value'])

#Clean up connection-scans data
try:
    es.indices.get("connection-scans")
    es.indices.delete("connection-scans")
except:
    pass
es.indices.create(index="connection-scans",body=json.loads(open(args.mapping_file,'r').read()))

#params in miliseconds
time_window=1200000
time_period=60000

watcher = WatcherClient(es)
watch_file=open(args.watch_file,'r')
watch_query=watch_file.read()
#start watching after time_window amount of data has passed
upper_time=min_time+time_window
while upper_time < max_time:
    new_query=watch_query.replace('%{upper_time}',str(upper_time)).replace('%{time_period}',str(int(time_period/60000)))
    lower_time=upper_time-time_window
    new_query=new_query.replace('%{lower_time}',str(lower_time))
    print ("running from %s to %s with period %s secs"%(lower_time,upper_time,time_period/1000))
    watch=json.loads(new_query)
    watcher.put_watch(id="port_scan",body=watch)
    watcher.execute_watch("port_scan")
    upper_time=upper_time+time_period



