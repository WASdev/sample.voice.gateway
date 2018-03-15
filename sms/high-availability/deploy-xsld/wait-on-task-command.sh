#!/bin/sh
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
memberAddr=$1
taskID=$2
xsadminPass=$3

printf "  Waiting for task to complete "
err=`curl -s -k -u "xsadmin:${xsadminPass}" "https://${memberAddr}:9445/wxsadmin/v1/task/${taskID}/status" -X GET`
isError=`echo ${err} | grep error | wc -l`
isSuccess=`echo ${err} | grep Success | wc -l |  tr -d ' '`
isRunning=`echo ${err} | grep Running | wc -l |  tr -d ' '`

while [ "${isError}" -eq "0" ] && [ "${isSuccess}" -eq "0" ] || [ "${isRunning}" -ne "0" ]
do
    printf '.'
	sleep 20
	err=`curl -s -k -u "xsadmin:${xsadminPass}" "https://${memberAddr}:9445/wxsadmin/v1/task/${taskID}/status" -X GET`
    isError=`echo ${err} | grep error | wc -l`
	if [ "${isError}" -eq "0" ]; then
        # Count "Failed" string as error
        isFailedTaskStatus=`echo ${err} | grep "Failed\"" | wc -l`
        if [ "${isFailedTaskStatus}" -ne 0 ]; then
                isError=1
        fi
    elif [ "${isError}" -ne "0" ]; then
		# Don't count the error if failed to get status because this happens during derby replication
		isFailedTaskStatus=`echo ${err} | grep "Failed to get the task status" | wc -l`
		if [ "${isFailedTaskStatus}" -ne 0 ]; then
			isError=0
		fi
		# Count "Failed" string as error
		isFailedTaskStatus=`echo ${err} | grep "Failed\"" | wc -l`
		if [ "${isFailedTaskStatus}" -ne 0 ]; then
			isError=1
		fi
	fi
	isSuccess=`echo ${err} | grep Success | wc -l |  tr -d ' '`
    isRunning=`echo ${err} | grep Running | wc -l |  tr -d ' '`
done
echo

if [ "${isError}" -eq "1" ]; then
	echo "  Task failed `date +"[%m-%d-%y-%T]"`"
	exit 1
elif [ "${isSuccess}" -eq "1" ]; then
	echo "  Task succeeded `date +"[%m-%d-%y-%T]"`"
fi
