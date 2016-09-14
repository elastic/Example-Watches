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
        es.indices.delete(test['index'])
    except:
        pass
    with open(test['mapping_file'],'r') as mapping_file:
        body=json.loads(mapping_file.read())
        es.indices.create(index=test["index"],body=body)
    #Index data
    current_data=last_time=datetime.datetime.utcnow()
    i=0
    for event in test['events']:
        #All offsets in seconds
        event_time=current_data+datetime.timedelta(seconds=int(event['offset']))
        event["@timestamp"]=event_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        es.index(index=test['index'],doc_type=test['type'],body=event,id=event['id'] if "id" in event else i)
        i+=1
    es.indices.refresh(index=test["index"])
    #Load Watch and Execute
    watcher = WatcherClient(es)
    with open(test['watch_file'],'r') as watch_file:
        watch=json.loads(watch_file.read())
        watcher.put_watch(id=test["watch_name"],body=watch)
        response=watcher.execute_watch(test["watch_name"])
        #Confirm Matches
        match = test['match'] if test['match'] else True
        print "Expected: Watch Condition: %s"%match
        met=response['watch_record']['result']['condition']['met']
        print "Received: Watch Condition: %s"%met
        if match:
            if met and response['watch_record']['result']['condition']['status'] == "success":
                print "Expected: %s"%test['expected_response']
                print "Received: %s"%response['watch_record']['result']['actions'][0]['logging']['logged_text']
                if response['watch_record']['result']['actions'][0]['logging']['logged_text'] == test['expected_response']:
                    print "TEST PASS"
                    sys.exit(0)
                else:
                    print "TEST FAIL"
                    sys.exit(1)
            else:
                print "TEST FAIL"
                sys.exit(1)
        else:
            print "TEST %s"%("PASS" if not response['watch_record']['result']['condition']['met'] else "FAIL")
            sys.exit(met)