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

function validateGridFile() {
    # Check grid file
    gridFile=grid-smsgw.json
    if [ ! -f "$gridFile" ]; then
        echo "Grid file: '$gridFile' was not found."
        exit 1;
    fi
}

function addGrid() {
    printStep "Creating grid..."
    # Add grids
    gridname=SMSGW_GRID
    gridFile=grid-smsgw.json
    echo "  Creating grid ${gridname}"

    taskID=$(curl -s -k -u "xsadmin:${xsadminPass}" "https://${masterIP}:9445/wxsadmin/v1/grid/${gridname}" -H "Content-Type:application/json" "-d@${gridFile}" -X POST)
    taskID=$(echo "${taskID}" | cut -d':' -f2 | cut -d'}' -f1)
    waitOnTaskCommand "${masterIP}" "${taskID}" "${xsadminPass}" "Creating Grid."
    printStep "Completed, grid created."
    echo
}
function loadCatalogServerIdentities() {
    xsldServerIPs=$(kubectl get pods -o wide | grep ${deploymentName} | awk '{ print $6 }')
    masterIP=$(echo ${xsldServerIPs} | cut -d' ' -f1)
}

function copyDependencies() {
    printStep "Copying dependencies..."
    sleep 10
    xsldPods=($(kubectl get pods -l service=${deploymentName} | grep Running | cut -d' ' -f1))
    for (( i=${#xsldPods[@]}-1; i >= 0; i-- )); do
        xsldPod=${xsldPods[i]}
        echo "  Copying dependencies in ${xsldPod}..."
        kubectl exec -it "${xsldPod}" /opt/tmp/copyDependencies.sh
        returnValue=$?
        if [ "$returnValue" -ne 0 ]; then
            log_error "Failed to copy dependencies."
            exit 1
        fi
    done
    printStep "Completed, dependencies copied."
    echo
}

function restartXSLDServers() {
    printStep "Restarting ${deploymentName} servers, this may take a while..."
    xsldAddresses=$(kubectl get pods -o wide | grep ${deploymentName} | awk '{ print $6 }')
    masterIP=$(echo ${xsldAddresses} | cut -d' ' -f1)
    sleep 10
    taskID=$(curl -k -s -u "xsadmin:${xsadminPass}" "https://${masterIP}:9445/wxsadmin/v1/task" -d "{\"command\":\"RestartServersTaskCommand\",\"description\":\"restart wxs\",\"parameters\":{\"restartGridServers\":\"true\", \"memberName\": \"${masterIP}\"}}" -H "Content-Type:application/json" -X POST)
    taskID=$(echo "${taskID}" | cut -d':' -f2 | cut -d'}' -f1)
    waitOnTaskCommand "${masterIP}" "${taskID}" "${xsadminPass}" "Restarting vgw-xsld Servers."
    returnValue=$?

    printStep "Completed, vgw-xsld servers restarted."
    echo
}

function waitOnTaskCommand() {
    local xsldAddress=$1
    local taskID=$2
    local xsAdminPassword=$3
    local errorMessage=$4
    ./wait-on-task-command.sh "${xsldAddress}" "${taskID}" "${xsAdminPassword}"

    returnValue=$?
    if [ "$returnValue" -ne 0 ]; then
        log_error "$errorMessage"
        exit 1
    fi
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
validateGridFile
loadCatalogServerIdentities

addGrid
copyDependencies
restartXSLDServers

