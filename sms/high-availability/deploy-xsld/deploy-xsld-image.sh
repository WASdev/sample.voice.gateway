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

deploymentName=vgw-xsld
# The location of the kubernetes deployment manifest for XSLD
deploymentManifest="./deploy-sms-xsld.json"

MAX_REPLICAS=3
KUBERNETES_XSLD_SECRET_NAME=${deploymentName}-secret
# Verify prereqs
error=0
if ! which kubectl; then
	echo 'kubectl is not present in this environment'
	error=1
fi
if [ ! -f "${deploymentManifest}" ]; then
	echo "The deployment manifest is not present at ${deploymentManifest}"
	error=1
fi

# Exit if an error was encountered
if [ ${error} -ne 0 ]; then
	exit 1
fi

function askForAdminUser() {
    echo "For the default XSLD Admin User \"xsadmin\". Enter a password (default: vgwAdmin4xs!): "
    read -rs xsadminPass
    xsadminPass=${xsadminPass:-vgwAdmin4xs!}
}

function askForNumberOfInstances() {
    echo "Getting number of schedulable worker nodes using 'kubectl get nodes'..."
    schedulableNodes=$(kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.taints[0].effect}{"\n"}{end}' | grep -cv 'NoSchedule')
    if [ "$schedulableNodes" -gt "$MAX_REPLICAS" ];
    then
        schedulableNodes=$MAX_REPLICAS;
    fi

    read -rp "Enter the number of XSLD instances (default instances: ${schedulableNodes}): " inputReplicas
    inputReplicas=${inputReplicas:-$schedulableNodes}
    if [ "$inputReplicas" -gt "$schedulableNodes" ] || [ "$inputReplicas" -le 0 ];
    then
        echo "Number of XSLD instances entered: ${inputReplicas} must be between 1 than ${schedulableNodes}."
        exit 1;
    fi

    maxReplicas=${inputReplicas:-$schedulableNodes}
    echo "Using ${maxReplicas} replicas."
}

function createXSLDKubernetesSecret() {
    NotFound=$(kubectl get secret vgw-xsld-secret 2>&1 | grep -c NotFound)
    if [ "$NotFound" -eq 0 ];
    then
        kubectl delete secret ${KUBERNETES_XSLD_SECRET_NAME}
    fi
    kubectl create secret generic "${KUBERNETES_XSLD_SECRET_NAME}" --from-literal=xsadminPass="${xsadminPass}" --from-literal=secretKey="${secretKey}"
}
# Deploy the manifest
function deployKubernetes() {
    kubectl create -f "${deploymentManifest}"
    kubectl scale "deployments/${deploymentName}" --replicas="${maxReplicas}"
}

function validateFiles() {
    # Check grid file
    gridFile=grid-smsgw.json
    if [ ! -f "$gridFile" ]; then
        echo "Grid file: '$gridFile' was not found."
        exit 1;
    fi
    # Check deployment manifest json file
    if [ ! -f "$deploymentManifest" ]; then
        echo "Voice Gateway XSLD deployment manifest file: '$deploymentManifest' was not found."
        exit 1;
    fi

    deploymentPropertiesFile=deploy.config
    if [ ! -f "$deploymentPropertiesFile" ]; then
        echo "Deployment properties file: '$deploymentPropertiesFile' was not found."
        exit 1;
    fi
}
validateFiles

if [ ! -z "$1" ]; then
    xsadminPass=$1
elif [ -z "$xsadminPass" ]; then
    askForAdminUser
fi
secretKey=$xsadminPass

askForNumberOfInstances
createXSLDKubernetesSecret
deployKubernetes
