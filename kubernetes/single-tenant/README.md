# Deploying IBM Voice Gateway on Bluemix Kubernetes cluster or Kubernetes on a VM or on IBM Cloud private
Running the IBM Voice Gateway in a Kubernetes environment requires special considerations beyond the deployment of a typical HTTP based application. Because the voice gateway relies on SIP for call signaling and RTP for media which require affinity to a specific voice gateway instance, the Kubernetes ingress router needs to be avoided for these protocols. To work around the limitations of the ingress router, the voice gateway containers must be configuered in net Host mode, which means that when a port is opened in either of the voice gateway containers, those identical ports are also opened and mapped on the base VM. This also eliminates the need to define media port ranges in the kubectl configuration file which is not currently supported.

In Kubernetes terminology, a single voice gateway instance equates to a single Pod which contains both a SIP Orchestrator container and a Media Relay container. Only one POD should be deployed per node and the POD should be deploy with hostNetwork set to true. This will ensure that the SIP and media ports would be opened on the host VM and visible by the SIP Load Balancer.  

## Script defaults:

* Enforces one POD per node. If replicas (PODs > #nodes, the extra replica to be scheduled will remain in a waiting state)
* Exposes SIP and media relay ports on the associated VM by setting hostNetwork to true
* Auto restart of any failed containers
* Creates a 2 GB persistent volume called recordings to store call recordings
* Recording is disabled by default. To enable recording set the value of ENABLE_RECORDING variable to true


# Deploying Voice Gateway in single-tenant mode:

1) Edit the deploy.yaml file and add your WATSON_CONVERSATION_WORKSPACE_ID.

1) Create a secret for the Watson service APIKEYs using the following command (make sure to use your own APIKEY):
   ```bash
   kubectl create secret generic secret-creds \
   --from-literal=WATSON_STT_APIKEY='aaaBBBcc2hskx44mdcdd_Ind3' \
   --from-literal=WATSON_TTS_APIKEY='aaaBBBcc2hskx44mdcdd_Ind3' \
   --from-literal=WATSON_CONVERSATION_APIKEY='aaaBBBcc2hskx44mdcdd_Ind3'
   ```

1) If you want to enable recording (Optional): 
   - Set ENABLE_RECORDING to true in deploy.yaml and create the recording [PersistentVolume and PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) using the recording-pv.yaml and recording-pvc.yaml templates.
   - Update the recording template files  and run the following commands: 
     ```bash
     kubectl create -f recording-pv.yaml
     kubectl create -f recording-pvc.yaml
     ```
   - Uncomment recording volume and volumeMounts sections of the deploy.yaml

1) If you want to use MRCPv2 config file (Optional):
   - More info: [Configuring services with MRCPv2](https://www.ibm.com/support/knowledgecenter/SS4U29/MRCP.html)
   - Create unimrcpConfig secret from the unimrcpclient.xml file using the following command: 
    ```bash
    kubectl create secret generic unimrcp-config-secret --from-file=unimrcpConfig=unimrcpclient.xml
    ```
   - Uncomment the unimrcpconfig volume and volumeMounts sections of the deploy.yaml 
  
1) Deploy on ICP:  
   ```bash
   kubectl create -f deploy.yaml
   ```