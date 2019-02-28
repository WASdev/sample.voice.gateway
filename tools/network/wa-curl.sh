#!/bin/bash

while true
    do
        curl -i -s -X POST \
            -u "username":"password" \
            --header "Content-Type:application/json" \
            --write-out ' \nlookup:        %{time_namelookup}\nconnect:       %{time_connect}\nappconnect:    %{time_appconnect}\npretransfer:   %{time_pretransfer}\nredirect:      %{time_redirect}\nstarttransfer: %{time_starttransfer}\ntotal:         %{time_total}\n' \
            --data "{\"input\": {\"text\": \"\"}}" "https://gateway.watsonplatform.net/conversation/api/v1/workspaces/workspace-id/message?version=2018-02-16" > ./result.txt
        
        tail -n 1 ./result.txt | awk '{
                if (2 < $NF) {
                    print strftime("time: %m/%d/%Y %H:%M:%S", systime())
                    system("cat result.txt")
                    print " "
                }
            }'
        sleep 2
    done


    
