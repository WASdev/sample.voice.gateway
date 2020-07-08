# Deploying IBM Voice Gateway on IBM Kubernetes Service, Kubernetes or OpenShift
Running the IBM Voice Gateway in a Kubernetes environment requires special considerations beyond the deployment of a typical HTTP based application. Because the Voice Gateway relies on SIP for call signaling and RTP for media which require affinity to a specific voice gateway instance, the Kubernetes ingress router needs to be avoided for these protocols. To work around the limitations of the ingress router, the voice gateway containers must be configuered in a `hostNetwork` mode, which means that when a port is opened in either of the voice gateway containers, those identical ports are also opened and mapped on the host machine. This also eliminates the need to define media port ranges in the kubectl configuration file which is not currently supported.

In Kubernetes terminology, a single voice gateway instance equates to a single Pod which contains both a SIP Orchestrator container and a Media Relay container. Only one POD should be deployed per node and the POD should be deploy with `hostNetwork` set to true. This will ensure that the SIP and media ports would be opened on the host VM and visible by the SIP Load Balancer.  

## In this repository

* [bluemix](https://github.com/WASdev/sample.voice.gateway/tree/master/kubernetes/bluemix) - Contains scripts for deploying IBM Voice Gateway on IBM Kubernetes Service

* [single-tenant](https://github.com/WASdev/sample.voice.gateway/tree/master/kubernetes/single-tenant) - Contains scripts for deploying IBM Voice Gateway in single-tenant mode on Kubernetes or Openshift

* [multi-tenant](https://github.com/WASdev/sample.voice.gateway/tree/master/kubernetes/multi-tenant) - Contains scripts for deploying Voice Gateway in multi-tenant mode on Kubernetes or Openshift


## Script details:

* The script deploys one POD per node. If #replicas > #nodes, the extra replicas to be scheduled will remain in a waiting state
* Exposes SIP and media relay ports on the associated VM by setting `hostNetwork` to true
* Auto restart of any failed containers
* It is recommended to use `oc` in place of `kubectl` for an Openshift cluster
* Increase `replica` if you have multiple nodes available
* To make the Voice Gateway pods to deploy on nodes of your choosing refer here: [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
* You can also change image tags from `latest` to the any specific version you want