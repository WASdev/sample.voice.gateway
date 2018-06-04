# Deploying IBM Voice Gateway on Bluemix Kubernetes cluster or Kubernetes on a VM or on IBM Cloud private
Running the IBM Voice Gateway in a Kubernetes environment requires special considerations beyond the deployment of a typical HTTP based application. Because the voice gateway relies on SIP for call signaling and RTP for media which require affinity to a specific voice gateway instance, the Kubernetes ingress router needs to be avoided for these protocols. To work around the limitations of the ingress router, the voice gateway containers must be configuered in net Host mode, which means that when a port is opened in either of the voice gateway containers, those identical ports are also opened and mapped on the base VM. This also eliminates the need to define media port ranges in the kubectl configuration file which is not currently supported.

In Kubernetes terminology, a single voice gateway instance equates to a single Pod which contains both a SIP Orchestrator container and a Media Relay container. Only one POD should be deployed per node and the POD should be deploy with hostNetwork set to true. This will ensure that the SIP and media ports would be opened on the host VM and visible by the SIP Load Balancer.  

## Script defaults:

* Enforces one POD per node. If replicas (PODs > #nodes, the extra replica to be scheduled will remain in a waiting state)
* Exposes SIP and media relay ports on the associated VM by setting hostNetwork to true
* Auto restart of any failed containers
* Creates a 2 GB persistent volume called recordings to store call recordings
* Recording is disabled by default. To enable recording set the value of ENABLE_RECORDING variable to true

## Notes for SMS integration
* The port 9080 and port 9443 have been exposed which when required can be updated with new values using HTTPS_PORT and HTTP_PORT variables.
  If these variables are updated , please make the same port updates for "containerPort" and "hostPort" variables in "ports" respectively since hostNetwork is true.
* The HTTP_HOST variable value stays *
* In tenantConfig.json file provide the values to all attributes in "smsPipe".
* When both SMS gateway and Voice Gateway are deployed in the same Kubernetes cluster then the "url" value contains the SMS gateway service name i.e. sms-gateway, currently default in sample.
* When the SMS gateway and the Voice Gateway are deployed in the separate Kubernetes cluster then the "url" value contains the IP for the SMS gateway server or any proxy server which maps to the sms-gateway service.
* When the SMS gateway and the Voice Gateway are deployed in the separate Kubernetes cluster then update the calico.yaml file to expose the values of HTTPS_PORT and HTTP_PORT.

## To deploy Voice Gateway in multi-tenant mode:

* Configure properties in tenantConfig.json before deployment. For more information - [Configuring multi-tenancy](https://www.ibm.com/support/knowledgecenter/SS4U29/multitenancy.html)
* Create secret called tenantconfig from the file tenantConfig.json:

```bash
kubectl create secret generic tenantconfig --from-file=tenantConfig.json
```

* Create secret for the secret-certs from file yourKeyFileNamewExtension.

* Deploy the Voice Gateway:

```bash
kubectl create -f deploy-multitenant.json
```