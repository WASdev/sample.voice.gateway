#!/bin/bash
# Usage: ./handle-call-exit.sh $err
# err: the exit code from the sipp command
# The contents of this script assume the user is using New Relic to handle the call exit and send a metric to New Relic's events API
# This is meant to be changed to handle he sipp error code and send an equivalent alert to the user's preferred metrics / alerting service
#
# NR_APIKEY="XXXX"
# NR_EVENTS_ENDPOINT="https://insights-collector.newrelic.com/v1/accounts/NR_ACCOUNT_ID/events"

if [ -z $NR_APIKEY ] || [ -z $NR_EVENTS_ENDPOINT ]; then
	echo 'Authentication or metrics endpoint were not set to handle the call exit code' 
	echo 'This code requires NR_APIKEY and NR_EVENTS_ENDPOINT to be set to the New Relic API key and the events API URL respectively'
	exit
fi

if [ "$1" = "0" ]; then
	eventSeverity=3
	eventDescription="The call was successful"
fi

metrics="[{
        \"eventType\": \"callMonitor\",
        \"severity\": \"${eventSeverity}\",
        \"description\": \"${eventDescription}\"
    }]"

echo "Sending to New Relic: $metrics"
curl -d "$metrics" -X POST -H "Content-Type: application/json" -H "X-Insert-Key: ${NR_APIKEY}" ${NR_EVENTS_ENDPOINT}


