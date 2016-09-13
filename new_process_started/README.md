# First Execution of a Process

## Description

A watch aims to alert if a process is started on a server for the first time.
 
The watch examines the previous N minutes for started processes.  This list is in turn used to search data older than N minutes, to see if the processes have been historically started.
Any differences result in an alert.

## Mapping Assumptions

A mapping is provided in mapping.json.  Watches require data producing the following fields:

* @timestamp (date field) - Date of log message.
* process_host - Contains the process name and host on which the process was started as a concatenated string e.g. testServerA_testServerB.  Watch assumes the delimiter is an _ char.
* event_type (non-analyzed string) - Contains the type for an event.  Indicates a process has started with the value “process_started”.

## Data Assumptions

The watch assumes each document in Elasticsearch represents a process event on a server.

## Demo Data

In addition to the usual tests, two test data sets are provided for demonstration purposes in the demo_data folder.

### Demo 1 - A metricbeat and ingest pipeline configuration configuration is provided.  This can be used to monitor processes on a local server and thus demonstrate the alert locally. A utility script 'load_ingest_pipeline.sh" loads the ingest pipeline to a locally hosted Elasticsearch instance. The user is required to load the watch (using load_watch.sh new_process_started) and [execute](https://www.elastic.co/guide/en/watcher/current/api-rest.html#api-rest-execute-watch) as required.

## Other Assumptions

* All events are index "log" and type "log".

# Configuration

The following watch metadata parameters influence behaviour:

* window_period - The period N (mins) over which the watch checks for newly started processes.  This should be equal to the scheduled interval.  Defaults to 30s.