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

function waitForPods() {
    runningPods=$(kubectl get pods -l service="${deploymentName}" --no-headers | grep Running | wc -l | awk '{print $1}')
    maxReplicas=$(kubectl get deployment vgw-xsld -o jsonpath='{.spec.replicas}')
    echo "${maxReplicas} replica(s) max"
    echo "${runningPods} running ${deploymentName} pods"

    printStep "Waiting for ${deploymentName} pods to be running..."
    # Wait for all pods to be running
    retries=620
    printf "  Checking ..."
    while [ "${retries}" -gt 0 ] && [ ! "${runningPods}" = "${maxReplicas}" ]; do
        retries=$((retries-1))
        printf '.'
        sleep 30
        runningPods=$(kubectl get pods -l service="${deploymentName}" --no-headers | grep Running | wc -l | awk '{print $1}')
    done
    if [ ${retries} -le 0 ] && [ "${runningPods}" -ne "${maxReplicas}" ]; then
        pods=$(kubectl get pods -l service=${deploymentName} --no-headers | cut -d' ' -f1)
        printf "Failed: Current pod deployment status: \n";
        echo
        kubectl get pods -l service=${deploymentName} --no-headers
        echo
        printf "Check for pod status or errors by running: \n"
        for pod in ${pods}; do
            echo -e "\tkubectl describe pod ${pod}"
        done
        echo "Timed out waiting for all ${deploymentName} pods to start on available nodes"
        # kubectl get pod | grep "${deploymentName}"
        exit 1
    fi

    printStep "Completed, ${deploymentName} pods running."
    echo
}

function waitForXSLDContainers() {
    printStep "Waiting for ${deploymentName} to start..."
    pods=$(kubectl get pods -l service=${deploymentName} | grep Running | cut -d' ' -f1)
    for pod in ${pods}; do
        printf "  Waiting for vgw-xsld to start on ${pod} `date +"[%m-%d-%y-%T]"` "
        nannyLogFile=/opt/ibm/WebSphere/eXtremeScale/wlp/startscripts/nanny/log/nanny.log
        kubectl exec -i ${pod} -- bash -c "cat ${nannyLogFile} | grep -i 'status to Online'" &> /dev/null
        err=$?
        delay=20
        retries=30
        while [ ! "${err}" = "0" ] && [ "${retries}" -gt 0 ]
        do
            sleep $delay
            kubectl exec -i ${pod} -- bash -c "cat ${nannyLogFile} | grep -i 'status to Online'" &> /dev/null
            err=$?
            retries=$((retries-1))
            printf '.'
        done
        if [ ${retries} -le 0 ]; then
            echo "Failed waiting for XSLD to start on ${pod}, troubleshoot the startup log: "
            echo
            echo "\t kubectl exec ${pod} -- cat ${nannyLogFile}"
            echo
            exit 1
        fi
        echo
        echo "  vgw-xsld has started on ${pod} `date +"[%m-%d-%y-%T]"`"
    done
    printStep "Completed, ${deploymentName} containers have started."
    echo
}

function printStep() {
    stepName=$1
    echo "Step: $stepName"
}

waitForPods
waitForXSLDContainers

