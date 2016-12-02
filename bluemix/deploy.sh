#!/bin/bash

# Image names
SO=voice-gateway-so
MR=voice-gateway-mr

#Image versions
SO_V="beta.latest"
MR_V="beta.latest"

#Container names
SO_NAME=voice-gateway-so
MR_NAME=voice-gateway-mr

CWD=$(PWD)

function usage() {
  cat <<EOF
 deploy.sh -S so_version -M mr_version
  -S so_version Version of Sip Orchestrator to deploy
  -M mr_version Version of Media Relay to deploy

	-----------------------------------------------------------------
  Example:
	-----------------------------------------------------------------
  deploy.sh
    -- Defaults to deploying SO:SO_V and MR:MR_V
  
  deploy.sh -S 0.1.0 -M 0.1.1
    -- Requires a SO:0.1.0
    -- Requires a MR:0.1.1
EOF
}

OPTIND=1
version=latest

while getopts ":S:M:" opt; do
  case $opt in
    S)
      SO_V=$OPTARG
      ;;
    M)
      MR_V=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      usage >&2
      exit 1
      ;;
  esac
done

shift "$((OPTIND-1))" # shift off the options...

# 1. Confirm we are logged in
echo "--------------------------------------------------------"
echo "  Deploying environment with version: ${version}"
echo "  Using API: "
cf target
if [ $? -ne 0 ];then echo "Not logged into Bluemix"; exit 1;fi

# 2. Initialize the CaaS (and get the Repository name)  We have trim the spaces off it 
REPO=$(cf ic init | awk -F: '/Bluemix registry/ {print $2}'| tr -d '[[:space:]]')
if [ $? -ne 0 ];then echo "Login to CAAS failed"; exit 1;fi

if [ "$REPO" == "" ]; then
   echo "Unable to determine the repository: $REPO"
   exit 1
else 
  echo "   Using REPO: $REPO"
fi
echo "--------------------------------------------------------"

# 3. get IP Addresses

echo "----> Determining IP Addresses"
IPS=$(cf ic ip list -q)
NUM_IPS=$(echo $IPS| wc -w);
while [ $NUM_IPS -lt 2 ]; do
  cf ic ip request
  IPS=$(cf ic ip list -q)
  NUM_IPS=$(echo $IPS| wc -w)
done
MR_IP=$(echo $IPS| awk '{print $1}')
SO_IP=$(echo $IPS| awk '{print $2}')
# NOTE:  We should probably UNBIND the IPs rather than just let them get removed.  It
# seems that removing a container bound to an IP may release the IP.  We might be better
# just doing an 'unbind' on the IP (but we have to have container ID too) so it is a tad
# more complicated.

echo "---------------------------------------------------"
echo " ${MR} IP will be: ${MR_IP}"
echo " ${SO} IP will be: ${SO_IP}"
echo "---------------------------------------------------"


#=======================================
# Deal with volumes
#=======================================
VOLUME_MOUNT="/cgw-media-relay/recordings"
VOLUME_ARG=""
VOLUME_NAME=""
echo "Currently in directory ${PWD}"
if [ -e docker.env ]; then
  VOLUME_NAME=$(awk -F= '/CF_VOLUME_NAME/ {print $2}' docker.env)
fi

if [ "$VOLUME_NAME" != "" ]; then
  cf ic volume list | grep $VOLUME_NAME
  if [ $? -ne 0 ]; then
    echo "** Creating a recording volume: ${VOLUME_NAME}, may take a while"
    cf ic volume create $VOLUME_NAME
  else
    echo "** Recording volume already exist: ${VOLUME_NAME}:${VOLUME_MOUNT}"
  fi
  VOLUME_ARG="--volume ${VOLUME_NAME}:${VOLUME_MOUNT}"
  echo "** Should use arguments for volume: ${VOLUME_ARG}"
fi

echo "** Removing existing containers..."
cf ic rm -f ${MR_NAME} >/dev/null
cf ic rm -f ${SO_NAME} >/dev/null
# Need to sleep so that we can wait for things to go away...
sleep 10 
echo "** Deploying the ${MR_NAME}"
echo "** Starting up ${MR_NAME}"
cf ic run -p 8080:8080 -p 16384-16484:16384-16484/udp -m 512 --name ${MR_NAME}\
  ${VOLUME_ARG} \
  --env WATSON_RELAY_SDP_ADDRESS=${MR_IP} \
  --env-file docker.env ${REPO}/${MR}:${MR_V}
echo "** Deploying the ${SO_NAME}"
echo "** Starting up ${SO_NAME}"
cf ic run -p 8080:8080 -p 5060:5060 -p 5060:5060/udp -m 512 --name ${SO_NAME} \
--env SIP_HOST=${SO_IP} \
--env RTP_RELAY_HOST=${MR_IP}:8080 \
--env-file docker.env ${REPO}/${SO}:${SO_V}
cf ic wait-status ${MR_NAME}
cf ic wait-status ${SO_NAME}
sleep 5
echo "** Binding IPS"
cf ic ip bind ${MR_IP} ${MR_NAME}
cf ic ip bind ${SO_IP} ${SO_NAME}
echo "** Showing IP Bindings"
cf ic ip list
echo "** Finished ** "
cf ic ps -a
