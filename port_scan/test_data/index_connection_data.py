__author__ = 'dalem@elastic.co'

from elasticsearch import Elasticsearch
import argparse
import datetime
import json
from elasticsearch import helpers

parser = argparse.ArgumentParser(description='Index Connection Log data into ES with the last event at the current time')
parser.add_argument('--host',help='host name')
parser.add_argument('--port',help='port')
parser.add_argument('--offset',help='time offset')
parser.add_argument('--file',help='input file')
parser.add_argument('--mapping_file',help='mapping file')
parser.set_defaults(host='localhost',port="9200",file='sample_conn.log',mapping_file='mapping.json')

args = parser.parse_args()


def getOffset(file_object):
    first = file_object.readline().decode().split("\t")
    file_object.seek(-2,2)
    while file_object.read(1) != b"\n":
        file_object.seek(-2,1)
    last = file_object.readline().decode().split("\t")
    return int(last[0][0:14].replace(".",""))-int(first[0][0:14].replace(".",""))

def read_file(file_object,offset):
    l_event_time=None
    last_time=None
    i=0
    for line in file_object:
        fields = line.split("\t")
        event_time=fields[0][0:14].replace(".","")
        if l_event_time is None:
            l_event_time=int(event_time)
            last_time=datetime.datetime.utcnow()-datetime.timedelta(milliseconds=offset)
        else:
           time_diff=int(event_time)-l_event_time
           l_event_time=int(event_time)
           last_time=last_time+datetime.timedelta(milliseconds=time_diff)
        yield {
            "@timestamp":last_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "host":fields[1],
            "source_ip":fields[2],
            "source_port":int(fields[3]),
            "dest_ip":fields[4],
            "dest_port":int(fields[5]),
            "source_dest_port":fields[2]+"_"+fields[4]+"_"+fields[5],
            "source_dest":fields[2]+"_"+fields[4],
            "_index" : "connection",
            "_type" : "connection"
        }
        i+=1
        if i % 100000 == 0:
            print("Loaded %s"%i)
    print("Loaded %s"%i)
    file_object.close()

es = Elasticsearch([args.host+":"+args.port])
conn_file=open(args.file,'rb')
offset=getOffset(conn_file)
conn_file.close()
try:
    es.indices.get("connection")
    es.indices.delete("connection")
except:
    pass
es.indices.create(index="connection",body=json.loads(open(args.mapping_file,'r').read()))
helpers.bulk(es,read_file(open(args.file,'r'),offset),chunk_size=500)
conn_file.close()