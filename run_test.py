import sys

__author__ = 'dalem@elastic.co'

import datetime
from elasticsearch_watcher import WatcherClient
from elasticsearch import Elasticsearch
import argparse
import json

parser = argparse.ArgumentParser(description='Index Connection Log data into ES with the last event at the current time')
parser.add_argument('--host',help='host name')
parser.add_argument('--port',help='port')
parser.add_argument('--test_file',help='test file')

parser.set_defaults(host='localhost',port="9200",test_file='data.json')
args = parser.parse_args()
es = Elasticsearch([args.host+":"+args.port])
with open(args.test_file,'r') as test_file:
    test=json.loads(test_file.read())
    #Load Mapping
    try:
        es.indices.get(test['index'])
        es.indices.delete(test['type'])
    except:
        pass
    with open(test['mapping_file'],'r') as mapping_file:
        es.indices.create(index=test["index"],body=json.loads(mapping_file.read()))
    #Index data
    current_data=last_time=datetime.datetime.utcnow()
    for event in test['events']:
        #All offsets in seconds
        event_time=current_data+datetime.timedelta(seconds=int(event['offset']))
        event["@timestamp"]=event_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        es.index(index=test['index'],doc_type=test['type'],body=event)
    es.indices.refresh(index=test["index"])
    #Load Watch and Execute
    watcher = WatcherClient(es)
    with open(test['watch_file'],'r') as watch_file:
        watch=json.loads(watch_file.read())
        watcher.put_watch(id=test["watch_name"],body=watch)
        response=watcher.execute_watch(test["watch_name"])
        #Confirm Matches
        if response['watch_record']['result']['condition']['met'] and response['watch_record']['result']['condition']['status'] == "success" and response['watch_record']['result']['actions'][0]['status'] == 'success':
            print "Watch Successfully Executed"
            if response['watch_record']['result']['actions'][0]['logging']['logged_text'] == test['expected_response']:
                print "Response confirmed"
                print response['watch_record']['result']['actions'][0]['logging']['logged_text']
                sys.exit(0)
            else:
                print "Incorrect Response"
                print response['watch_record']['result']['actions'][0]['logging']['logged_text']
            sys.exit(1)
