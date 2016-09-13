# Example Watches

## Overview

This package provides a collection of example  watches.  These watches have been developed for the purposes of POC's and demonstrations.  Each makes independent assumptions as to the data structure, volume and mapping.  For each watch a description, with assumptions is provided, in addition to a mapping file.  Whilst functionally tested, these watches have not been tested for effectiveness or query performance in production environments.  The reader is therefore encouraged to test and review all watches with production data volumes prior to deployment.

#Generic Assumptions

* Elasticsearch 5.x
* All watches use the log output for purposes of testing. Replace with output e.g. email, as required.
* Painless inline script is enabled for clarity and testing only.  All scripts should be moved to hosted script (file or indexed) for production deployment.
* All watches assume Watcher is running in the same cluster as that in which the relevant data is hosted.  They all therefore use the search input.  In a production deployment this is subject to change i.e. a http input maybe required.

#Structure

In each watch directory the following is provided:

* README - describes the watch including any assumptions regards mapping, data structure and behaviour.
* mapping.json - An re-usable mapping which is also appropriate for the test data provided.
* watch.json - Body of the watch. Used in the below tests. 
* /tests - Directory of tests.  Each test is defined as JSON file.  See Below.
* load_watch.sh.  Utility script for loading each watch to a local Elasticsearch cluster.  Each watch can be loaded by running load_watch.sh <watch folder name>. 

The parent directory includes the following utility scripts:

* run_test.py - A python script which can be used to run a specific test e.g. python run_test.py --test_file new_process_started/tests/test1.json 
* load_watch.sh - Utility script for loading a specific watch to a local Elasticsearch cluster. The first parameter should specify the folder name e.g. ./load_watch.sh errors_in_logs
* run_all_tests.sh - Runs all tests and prints output.

#Watches

* Errors in log files - A watch which alerts if errors are present in a log file. Provides example errors as output.
* Port Scan - A watch which aims to detect and alert if a server established a high number of connections to a destination across a large number of ports.
* Social Media Trending - A watch which alerts if a social media topic/tag begins to show increase activity
* Unexpected Account Activity - A watch which aims detect and to alert if a user is created in Active Directory/LDAP and subsequently deleted within N mins.
* New Process Started - A watch which aims to detect if a process is started on a server for the first time.
* New User-Server Communication - A watch which aims to detect if a user logs onto a server for the first time within the current time period.

#Testing

Each watch includes a test directory containing a set of tests expressed as JSON files.  Each JSON file describes a single isolated test and includes:

* watch_name - The watch name
* watch_file - Location of the watch file (relative to base directory)
* mapping_file - Location of the mapping file (relative to base directory)
* index - The required index on which both the watch and test depend.
* type - The required type on which both the watch and test depend.
* events - A list of test data objects.  Each test data object contains the required fields and an 'offset' value.  This integer can be positive and negative.  This value is added to the current system time when the events are indexed by the run_test.py.  To ensure the "past" is populated as required use negative values.  This ensures the test data is populated for the current period, allows the watches to match.
* match - A field indicating if the watch should match - defaults to true.

The run_test.py performs the following when running a test file:

1. Deletes the index specified.
2. Loads the required mapping.
3. Loads the dataset, setting the timestamps of the events to the current+offset.
4. Refreshes the index.
5. Adds the watch
6. Executes the watch
7. Confirms the watch matches the intended outcome. matched and confirms the output of the watch (log text)




