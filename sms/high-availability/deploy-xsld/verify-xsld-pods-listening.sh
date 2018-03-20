#!/bin/bash
# *****************************************************************
#
# (C) Copyright IBM Corporation 2018.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# *****************************************************************
source ./deploy.config

function askForAdminUser() {
    echo "For the default XSLD Admin User \"xsadmin\". Enter a password (default: vgwAdmin4xs!): "
    read -rs xsadminPass
    xsadminPass=${xsadminPass:-vgwAdmin4xs!}
    secretKey=$xsadminPass
}

function waitForAdmin() {
    xsldServerIPs=$(kubectl get pods -o wide | grep ${deploymentName} | awk '{ print $6 }')
    printStep "Waiting for ${deploymentName} to listen for requests"
    for xsldServer in ${xsldServerIPs}; do
        printf "  Checking %s " "${xsldServer}"
        # Wait for
        attempts=18
        until $(curl --silent --output /dev/null -u "xsadmin:${xsadminPass}" -k -X GET https://${xsldServer}:9445/wxsadmin/v1/task); do
            printf '.'
            sleep 10
            attempts=$((attempts-1))
            if [ "$attempts" -eq 0 ]; then
                log_error "Timed out waiting on ${deploymentName} to listen for requests"
                exit 1
            fi
        done
        echo
    done
    printStep "Completed, all ${deploymentName} servers are listening."
    masterIP=$(echo ${xsldServerIPs} | cut -d' ' -f1)

    echo "You can now access the dashboard of the master XSLD instance by accessing this url: https://${masterIP}:9443/wxsui, it can provide you information on the progess of tasks."
    echo
}

function printStep() {
    stepName=$1
    echo "Step: $stepName"
}
if [ ! -z "$1" ]; then
    xsadminPass=$1
elif [ -z "$xsadminPass" ]; then
    askForAdminUser
fi

waitForAdmin
