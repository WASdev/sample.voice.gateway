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

function askForAdminUser() {
    echo "For the default XSLD Admin User \"xsadmin\". Enter a password (default: vgwAdmin4xs!): "
    read -rs xsadminPass
    xsadminPass=${xsadminPass:-vgwAdmin4xs!}
    secretKey=$xsadminPass
}
if [ ! -z "$1" ]; then
    xsadminPass=$1
elif [ -z "$xsadminPass" ]; then
    askForAdminUser
fi
./deploy-xsld-image.sh "$xsadminPass"
./verify-xsld-pods-started.sh "$xsadminPass"
./verify-xsld-pods-listening.sh "$xsadminPass"
./join-xsld-members.sh "$xsadminPass"
./deploy-smsgw-grid-application.sh "$xsadminPass"
./get-catalog-endpoints-for-smsgw.sh
echo "Deployment Completed"

