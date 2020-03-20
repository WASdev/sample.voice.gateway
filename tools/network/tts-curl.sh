#!/bin/bash

TEXT_TO_SYNTHESIZE='Hello World!'
API_KEY='<API_KEY>'
API_ENDPOINT='https://stream.watsonplatform.net/text-to-speech/api'
VOICE='en-US_AllisonVoice'

# Time between requests, defaults to 1 minute
SLEEP_TIME=10
JSON_DATA="{\"text\":\"${TEXT_TO_SYNTHESIZE}\"}"

while true
    do

        curl -D ./headers.txt -i -s -X POST \
            -u "apikey":"$API_KEY" \
            --header "Content-Type: application/json" \
            --header "Accept: audio/wav" \
            --data "$JSON_DATA" \
            --output /dev/null \
            --write-out "\ndns_lookup: %{time_namelookup}\nconnect: %{time_connect}\nappconnect: %{time_appconnect}\npretransfer: %{time_pretransfer}\nredirect: %{time_redirect}\nstarttransfer: %{time_starttransfer}\ntotal: %{time_total}\n" \
            "$API_ENDPOINT/v1/synthesize?voice=$VOICE" > ./result.txt

        tail -n 1 ./result.txt | awk '{
                if (4 < $NF) {
                    print strftime("time: %m/%d/%Y %H:%M:%S", systime())
                    system("cat ./headers.txt | grep -v Authorization")
                    system("cat ./result.txt")
                    print " "
                }
            }'
        sleep $SLEEP_TIME
    done
