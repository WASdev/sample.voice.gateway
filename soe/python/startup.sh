#!/bin/bash

export CLOUDANT_URL="https://cb3fca4e-e0f6-4a7b-9a98-f3c8ed9d4820-bluemix:e7833b543725775f89ff1f0915c1f67135423a2d5b7746588ce99c2f9b72dc06@cb3fca4e-e0f6-4a7b-9a98-f3c8ed9d4820-bluemix.cloudant.com"
export CONVERSATION_PASSWORD="0oSVoDfHiQCl"
export CONVERSATION_USERNAME="9ff51c5e-5cb2-4877-b7ca-a7f3194ca8ba"
export CONVERSATION_VERSION="2017-04-21"
export CONVERSATION_WORKSPACE_ID="f7108771-4af5-4e26-b279-8721c82375b0"
export WEB_LOGGING="True"
python voiceProxyServer.py

