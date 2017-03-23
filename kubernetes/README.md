# Configuring IBM Voice Gateway High Availability in Kubernetes
Running the IBM Voice Gateway in a Kubernetes environment requires special considerations beyond the deployment of a typical HTTP based application. Because the voice gateway relies on SIP for call signaling and RTP for media which require affinity to a specific voice gateway instance, the Kubernetes ingress router needs to be avoided for these protocols. To work around the limitations of the ingress router, the voice gateway containers must be configuered in net Host mode, which means that when a port is opened in either of the voice gateway containers, those identical ports are also opened and mapped on the base VM. This also eliminates the need to define media port ranges in the kubectl configuration file which is not currently supported.

In Kubernetes terminology, a single voice gateway instance equates to a single Pod which contains both a SIP Orchestrator container and a Media Relay container. Only one POD should be deployed per node and the POD should be deploy with hostNetwork set to true. This will ensure that the SIP and media ports would be opened on the host VM and visible by the SIP Load Balancer.  

A sample JSON kubectl configuration file can be found here: [sample.voice.gateway.for.watson GitHub repository](https://github.com/WASdev/sample.voice.gateway.for.watson/tree/master/kubernetes)

Some of what's enabled by this kubectl config file include:

 - Three voice gateway Pods deployed across three separate nodes (add more nodes if needed by increasing replicas)
 - Enforces one POD per node. If replicas (PODs > #nodes, the extra replica to be scheduled will remain in a waiting state)
 - Exposes SIP and media relay ports on the associated VM by setting hostNetwork to true
 - Auto restart of any failed containers

## Working with IBM Spectrum Conductor for Containers (CfC)
Since CfC includes Kubernetes, the section above also applies when the IBM Voice Gateway is deployed on top of IBM Spectrum CfC. This section describes the procedure for pushing the voice gateway images into the CfC master repository.

Once the voice gateway images have been pulled locally, they can be pushed into the CfC master repository using these commands:

```bash
docker pull ibmcom/voice-gateway-so:latest 
docker pull ibmcom/voice-gateway-mr:latest
docker login https://master.cfc:8500 --username admin --password admin
docker tag ibmcom/voice-gateway-so:latest master.cfc:8500/admin/voice-gateway-so:latest
docker push master.cfc:8500/admin/voice-gateway-so:latest
docker tag ibmcom/voice-gateway-mr:latest master.cfc:8500/admin/voice-gateway-mr:latest
docker push master.cfc:8500/admin/voice-gateway-mr:latest
```  

