#!/bin/bash

export CLOUDANT_URL="https://{cloudant_account}:{password}@{cloudant_account}-bluemix.cloudant.com"
export CONVERSATION_PASSWORD="password"
export CONVERSATION_USERNAME="username"
export CONVERSATION_VERSION="2017-04-21"
export CONVERSATION_WORKSPACE_ID="f7108771-4af5-4e26-b279-8721c82375b0"
export WEB_LOGGING="True"
python voiceProxyServer.py

