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
}

function waitOnTaskCommand() {
    local xsldAddress=$1
    local taskID=$2
    local xsAdminPassword=$3
    local errorMessage=$4
    ./wait-on-task-command.sh "${xsldAddress}" "${taskID}" "${xsAdminPassword}"

    returnValue=$?
    if [ "$returnValue" -ne 0 ]; then
        echo "$errorMessage"
        exit 1
    fi
}

function joinMembers() {
    printStep "Joining Members, this may take a while..."
    for member in ${memberIPs}; do
        echo "  Joining ${member} to ${masterIP}"
        taskID=$(curl -s -k -u "xsadmin:${xsadminPass}" "https://${member}:9445/wxsadmin/v1/task" -d "{\"command\": \"NewMemberJoinTaskCommand\",\"description\": \"add a new member\",\"parameters\": {\"secretKey\": \"${secretKey}\",\"memberName\": \"${member}\",\"cacheMemberGroupHost\": \"${masterIP}\",\"isCatalog\": \"true\"}}" -H "Content-Type:application/json" -X POST)
        taskID=$(echo "${taskID}" | cut -d':' -f2 | cut -d'}' -f1)
        waitOnTaskCommand "${member}" "${taskID}" "${xsadminPass}" "Joining members failed, try cleaning up your deployment by running ./cleanupsms-xsld.sh, alternatively you can check the dashboard task progress and pull the logs as shown here https://www.ibm.com/support/knowledgecenter/en/SSTVLU_8.6.1/com.ibm.websphere.extremescale.doc/txstraceserverlogxsld.html"
    done
    printStep "Completed, above mentioned members joined."
    echo
}
function printStep() {
    stepName=$1
    echo "Step: $stepName"
}
function loadCatalogServerIdentities() {
    xsldServerIPs=$(kubectl get pods -o wide | grep ${deploymentName} | awk '{ print $6 }')
    masterIP=$(echo ${xsldServerIPs} | cut -d' ' -f1)
    memberIPs=$(echo ${xsldServerIPs} | cut -d' ' -f2-)
}


if [ ! -z "$1" ]; then
    xsadminPass=$1
elif [ -z "$xsadminPass" ]; then
    askForAdminUser
fi
secretKey=$xsadminPass

loadCatalogServerIdentities
joinMembers
