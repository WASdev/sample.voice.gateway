# IBM Voice Gateway Helm Chart

[IBM Voice Gateway](https://www.ibm.com/support/knowledgecenter/SS4U29/welcome_voicegateway.html) provides a way to integrate a set of orchestrated Watson services with a public or private telephone network by using the Session Initiation Protocol (SIP). Voice Gateway enables direct voice interactions over a telephone with a cognitive self-service agent or transcribes a phone call between a caller and agent so that the conversation can be processed with analytics for real-time agent feedback.

## Introduction

This chart will deploy IBM Voice Gateway

## Prerequisites

### Required
- Create following Watson services on IBM Cloud.
  - [Watson Speech to Text](https://www.ibm.com/watson/services/speech-to-text/)
  - [Watson Text to Speech](https://www.ibm.com/watson/services/text-to-speech/) (self-service only)
  - [Watson Conversation](https://www.ibm.com/watson/services/conversation/) or [Watson Virtual Agent](https://www.ibm.com/us-en/marketplace/cognitive-customer-engagement) (self-service only)
  
    **Important:** For the Conversation service, you'll need to add a workspace with a dialog. You can quickly get started by importing the [sample-conversation-en.json](https://github.com/WASdev/sample.voice.gateway/tree/master/conversation) file from your cloned sample.voice.gateway GitHub repository. To learn more about importing JSON files, see [Creating workspaces](https://console.bluemix.net/docs/services/conversation/configure-workspace.html#creating-workspaces) in the Conversation documentation. If you build your own dialog instead of using the sample, ensure that your dialog includes a node with the *conversation_start* condition and node with a default response.
  
- Configure tenantConfig.json and create Kubernetes Secret:
  - Get the sample [tenantConfig.json](https://github.com/WASdev/sample.voice.gateway/blob/master/kubernetes/multi-tenant/tenantConfig.json) file.
  - Fill in the service credentials. You can further customize it as per your needs. More details [here](https://www.ibm.com/support/knowledgecenter/SS4U29/multitenancy.html).
  - You can have 1 or more tenant.
  - Make sure you have [configured your kubectl client](https://www.ibm.com/support/knowledgecenter/SSBS6K_2.1.0/manage_cluster/cfc_cli.html). 
  - Run the following command. (Make sure you are in same directory as your tenantConfig.json file)
    ```
    kubectl create secret generic tenantconfig --from-file=tenantConfig.json
    ```


### Optional
- To Enable recording:
  - Change value of enableRecording to 'true'
  - PersistentVolume needs to be pre-created prior to installing the chart to enable recording. It can be created by using the IBM Cloud Private UI or via a yaml file as the following example: 
  
  ```
  kind: PersistentVolume
  apiVersion: v1
  metadata:
    name: recordings
    labels: {}
  spec:
    capacity:
      storage: 2Gi
    accessModes:
    - ReadWriteMany
    persistentVolumeReclaimPolicy: Retain
    hostPath:
      path: <PATH>
  ```

  **Important:** Make sure the name of PersistentVolume is `recordings`,  accessModes is `ReadWriteMany` and persistentVolumeReclaimPolicy is `Retain`.

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm install --name my-release stable/ibm-voice-gateway
```

## Uninstalling the Chart

- To uninstall/delete the `my-release` deployment:

  ```bash
  $ helm delete my-release
  ```

  The command removes all the Kubernetes components associated with the chart and deletes the release but keeps `my-release` in the release history.

- To uninstall/delete the `my-release` deployment as well as remove it from the release history:

  ```bash
  $ helm delete --purge my-release
  ```

