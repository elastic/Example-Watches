# Example Watches

## Overview

This package provides a collection of example  watches.  These watches have been developed for the purposes of POC's and demonstrations.  Each makes independent assumptions as to the data structure, volume and mapping.  For each watch a description, with assumptions is provided, in addition to a mapping file.  Whilst functionally tested, these watches have not been tested for effectiveness or query performance in production environments.  The reader is therefore encouraged to test and review all watches with production data volumes prior to deployment.

#Generic Assumptions

* Elasticsearch 5.x
* All watches use the log output for purposes of testing. Replace with output e.g. email, as required.
* Painless inline script is enabled for clarity and testing only.  All scripts should be moved to hosted script (file or indexed) for production deployment.
* All watches assume Watcher is running in the same cluster as that in which the relevant data is hosted.  They all therefore use the search input.  In a production deployment this is subject to change i.e. a http input maybe required.

#Structure

For each watch the following is provided:

* README - describes the watch including any assumptions regards mapping, data structure and behaviour.
* mapping.json - An approapriate mapping for the test data provided.
* watch.json - Body of the watch.
* /test_data - Directory of test data with instructions on loading and using the test set.
* load_watch.sh.  Utility script for loading each watch to a local Elasticsearch cluster.  Each watch can be loaded by running load_watch.sh <watch folder name>. 

#Watches

* Errors in log files - A watch which alerts if errors are present in a log file. Provides example errors as output.
* Port Scan - A watch which aims to detect and alert if a server established a high number of connections to a destination across a large number of ports.
* Social Media Trending - A watch which alerts if a social media topic/tag begins to show increase activity
* Unexpected Account Activity - A watch which aims detect and to alert if a user is created in Active Directory/LDAP and subsequently deleted within N mins.
* New Process Started - A watch which aims to detect if a process is started on a server for the first time.
* New User-Server Communication - A watch which aims to detect if a user logs onto a server for the first time within the current time period.