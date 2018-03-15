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

## Builds the XS_CATALOG_ENDPOINTS url from the WXS Pods
source ./deploy.config
CATALOG_IPs=($(kubectl get pods -o wide | grep ${deploymentName} | awk '{ print $6 }'))
CATALOG_ENDPOINTS=''

for (( i=0; i < ${#CATALOG_IPs[@]}; i++ )); do
    CATALOG_ENDPOINTS+="${CATALOG_IPs[i]}:4809"


    if [ $i -lt $((${#CATALOG_IPs[@]}-1)) ];
    then
        CATALOG_ENDPOINTS+=","
    fi
done

echo "Set XS_CATALOG_ENDPOINTS=${CATALOG_ENDPOINTS} in your SMS Gateway Deployment"
