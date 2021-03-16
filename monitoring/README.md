# Call monitoring
This folder contains resources necessary to build a docker image that will run a sipp call and send a result metric to a metric / alert processing service such as New Relic.
This image can then be run locally periodically or as a CronJob resource as part of an OpenShift or Kubernetes deployment

## Building and running the image
From the `monitoring` folder run the following command to build the image:
```
docker build -t voice-call-monitor .
```

Run the image:
```
docker run -it --net=host -e SBC_ADDR=10.10.10.10:5060 -e TENANT_NUMBER=18001112222 voice-call-monitor:latest
```



## Environment variables
The following environment variables need to be set for this script to run

### SBC_ADDR
The address of the session border controller or Voice Gateway SIP endpoint where the call will be placed to

Example value: SBC_ADDR=`10.10.10.10:5060`

### TENANT_NUMBER
The number to call

Example value: TENANT_NUMBER=`18001112222`


## Optional Environment variables
### LOCAL_IP
The script `voice-call-monitor.sh` will use the following command to try to determine the correct local interface IP to use to place the call
```
LOCAL_IP=$(hostname -I | cut -d' ' -f1)
```
This may not always be accurate, so the environment variable `LOCAL_IP` can be set to override this.


The following environment variables are only necessary to set if New Relic will be used to process metrics. Setting these will allow the script to send a `callMonitor` metric to New Relic

### NR_APIKEY
The API key for a New Relic account.

### NR_EVENTS_ENDPOINT
The events endpoint URL for a New Relic account

Example value: NR_EVENTS_ENDPOINT=`https://insights-collector.newrelic.com/v1/accounts/<<NR_ACCOUNT_ID>>/events`
- NOTE: `<<NR_ACCOUNT_ID>>` above needs to be replaced with a New Relic account ID
