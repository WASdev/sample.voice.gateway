# Deploying IBM Voice Gateway on Kubernetes/IBM Cloud private
Running the IBM Voice Gateway in a Kubernetes environment requires special considerations beyond the deployment of a typical HTTP based application. Because the voice gateway relies on SIP for call signaling and RTP for media which require affinity to a specific voice gateway instance, the Kubernetes ingress router needs to be avoided for these protocols. To work around the limitations of the ingress router, the voice gateway containers must be configuered in net Host mode, which means that when a port is opened in either of the voice gateway containers, those identical ports are also opened and mapped on the base VM. This also eliminates the need to define media port ranges in the kubectl configuration file which is not currently supported.

In Kubernetes terminology, a single voice gateway instance equates to a single Pod which contains both a SIP Orchestrator container and a Media Relay container. Only one POD should be deployed per node and the POD should be deploy with hostNetwork set to true. This will ensure that the SIP and media ports would be opened on the host VM and visible by the SIP Load Balancer.  

## In this repository

* [bluemix](https://github.com/WASdev/sample.voice.gateway/tree/master/kubernetes/bluemix) - Contains scripts for deploying Voice Gateway on Bluemix Kubernetes Cluster

* [single-tenane](https://github.com/WASdev/sample.voice.gateway/tree/master/kubernetes/single-tenant) - Contains scripts for deploying Voice Gateway in single-tenant mode on kubernetes in VM or ICp

* [multi-tenant](https://github.com/WASdev/sample.voice.gateway/tree/master/kubernetes/multi-tenant) - Contains scripts for deploying Voice Gateway in multi-tenant mode on kubernetes in VM or ICp


## Script defaults:

* Enforces one POD per node. If replicas (PODs > #nodes, the extra replica to be scheduled will remain in a waiting state)
* Exposes SIP and media relay ports on the associated VM by setting hostNetwork to true
* Auto restart of any failed containers