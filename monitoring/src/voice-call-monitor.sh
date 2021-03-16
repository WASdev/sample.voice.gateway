#!/bin/bash
# This script will use sipp to call a voice gateway endpoint
# Usage: ./voice-call-monitor.sh 
#
# SBC_ADDR=10.10.10.10:5060
# TENANT_NUMBER=18001112222

SIPP_SCENARIO='monitoring-test.xml'
if [ -z $LOCAL_IP ]; then
  LOCAL_IP=$(hostname -I | cut -d' ' -f1)
fi

cd /SIP/sipp-3.5.1/

# Call the voice agent
./sipp -sf $SIPP_SCENARIO $SBC_ADDR -s $TENANT_NUMBER -m 1 -users 1 -max_invite_retrans 4 -i $LOCAL_IP -trace_err -trace_msg -trace_screen > /dev/null
err=$?

/src/handle-call-exit.sh $err

tail -f /dev/null
