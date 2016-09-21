if [ -z "$1" ] ; then
    echo "No watch name supplied e.g. ./load_watch.sh port_scan"
    exit 1
fi

username=elastic
if [ "$2" ] ; then
  username=$2
fi

password=changeme
if [ "$3" ] ; then
  password=$3
fi

curl -s -o /dev/null -X DELETE localhost:9200/_xpack/watcher/watch/$1 -u $username:$password
es_response=$(curl --w "%{http_code}" -s -o /dev/null -X PUT localhost:9200/_xpack/watcher/watch/$1 -u $username:$password -d @$1/watch.json -H "Expect:")
if [ 0 -eq $? ] && [ $es_response = "201" ]; then
echo "Loading $2 watch...OK"
exit 0
else
echo "Loading $2 watch...FAILED"
exit 1
fi
