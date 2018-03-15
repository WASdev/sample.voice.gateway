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
set -e
source deploy.config

read -rp "Are you sure you wish to continue, this will erase any cached data and XSLD instances (Y/N)" confirm

if [ "$confirm" = "Y" ] || [ "$confirm" = "y" ]; then
    echo "Cleaning up..."
    pods=$(kubectl get pods | grep $deploymentName | grep Running | awk '{ print $1 }')
    if [ ${#pods[@]} -gt 0 ]; then
        for pod in $pods; do
            echo "Cleaning pod $pod..."
            kubectl exec -it "$pod" -- bash -c "rm -rf /vol/*"
        done
    fi
    kubectl delete deployment $deploymentName
else
    echo "Will not clean up the deployment."
fi
