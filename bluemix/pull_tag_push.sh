#!/bin/bash

# Image names
SO=voice-gateway-so
MR=voice-gateway-mr

#Image versions
SO_V="beta.latest"
MR_V="beta.latest"

#DockerHub repositories for original images
DOCKER_HUB_SO_REPO=ibmcom/voice-gateway-so
DOCKER_HUB_MR_REPO=ibmcom/voice-gateway-mr

function usage() {
  cat <<EOF
 tag_and_push.sh -S so_version -M mr_version
  -S so_version Version of Sip Orchestrator to use
  -M mr_version Version of Media Relay to use

	-----------------------------------------------------------------
  Example:
	-----------------------------------------------------------------
  pull_tag_push.sh
    -- Defaults to grabbing ${DOCKER_HUB_SO_REPO}:${SO_V} and ${DOCKER_HUB_MR_REPO}:${MR_V}
  
  pull_tag_push.sh -S 0.1.0 -M 0.1.1
    -- Requires a ${DOCKER_HUB_SO_REPO}:0.1.0
    -- Requires a ${DOCKER_HUB_MR_REPO}:0.1.1

    Will tag and push:
       REPO/${SO}:0.1.0
       REPO/${MR}:0.1.1
EOF
}

function image_exists() {
  if [ $(docker images $1 | wc -l) -gt 1 ]; then
		echo "FOUND"
  else
		echo ""
 fi
}

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

# 1. Confirm we are logged in
echo "--------------------------------------------------------"
echo "  Confirming you are logged in... "
cf target
if [ $? -ne 0 ];then echo "Not logged into Bluemix"; exit 1;fi

# Initialize the CaaS (and get the Repository name)  We have trim the spaces off it
REPO=$(cf ic init | awk -F: '/Bluemix registry/ {print $2}'| tr -d '[[:space:]]')
if [ $? -ne 0 ];then echo "Login to CAAS failed"; exit 1;fi

if [ "$REPO" == "" ]; then
   echo "Unable to determine the repository: $REPO"
   exit 1
else
  echo "   Using REPO: $REPO"
fi

if [ "$SO_V" == "" ]; then SO_V=${version};fi
if [ "$MR_V" == "" ]; then MR_V=${version};fi

echo "  From SO Image: ${SO}:${SO_V}"
echo "  From MR Image: ${MR}:${MR_V}"
echo "--------------------------------------------------------"

CWD=$(pwd)

echo "==============================================="
echo "  Pulling ${DOCKER_HUB_SO_REPO}:${SO_V}"
echo "  Tagging ${REPO}/${SO}:${SO_V}"
echo "  ... and pushing to repository .."
echo "  REPO: ${REPO}"
echo "==============================================="

docker pull "${DOCKER_HUB_SO_REPO}:${SO_V}"

if [ "$(image_exists ${DOCKER_HUB_SO_REPO}:${SO_V})" == "" ];then
  echo "Image ${DOCKER_HUB_SO_REPO}:${SO_V} does not exist";
  usage
  exit 1;
fi

docker tag "${DOCKER_HUB_SO_REPO}:${SO_V}" "${REPO}/${SO}:${SO_V}"
echo "** Pushing ${REPO}/${SO}:${SO_V}"
docker push ${REPO}/${SO}:${SO_V}

echo "==============================================="
echo "  Pulling ${DOCKER_HUB_MR_REPO}:${MR_V}"
echo "  Tagging ${REPO}/${MR}:${MR_V}"
echo "  ... and pushing to repository .."
echo "  REPO: ${REPO}"
echo "==============================================="

docker pull "${DOCKER_HUB_MR_REPO}:${MR_V}"

if [ "$(image_exists ${DOCKER_HUB_MR_REPO}:${MR_V})" == "" ];then
  echo "Image ${DOCKER_HUB_MR_REPO}:${MR_V} does not exist";
  usage
  exit 1;
fi

docker tag "${DOCKER_HUB_MR_REPO}:${MR_V}" "${REPO}/${MR}:${MR_V}"
echo "** Pushing ${REPO}/${MR}:${MR_V}"
docker push ${REPO}/${MR}:${MR_V}

echo "==================================================================="
echo "  Pull, tag and push of voice gateway images completed successfully"
echo "==================================================================="
