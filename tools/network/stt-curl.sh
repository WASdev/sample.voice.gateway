#!/bin/bash

while true
    do
        curl -i -s -X POST \
            -u "apikey:api-key-value" \
            --header "Content-Type:audio/wav" \
            --data-binary @resources/smoky-fires.wav \
            --write-out "\ndns_lookup: %{time_namelookup}\nconnect: %{time_connect}\nappconnect: %{time_appconnect}\n pretransfer: %{time_pretransfer}\nredirect: %{time_redirect}\nstarttransfer: %{time_starttransfer}\ntotal: %{time_total}\n" \
			"https://gateway-wdc.watsonplatform.net/speech-to-text/api/v1/recognize?model=en-US_NarrowbandModel" > ./result.txt
        
        tail -n 1 ./result.txt | awk '{
                if (4 < $NF) {
                    print strftime("time: %m/%d/%Y %H:%M:%S", systime())
                    system("cat result.txt")
                    print " "
                }
            }'
        sleep 2
    done
