![](https://raw.githubusercontent.com/WASdev/sample.voice.gateway.for.watson/master/images/VoiceGateway_WebLogo_Color-2.png)

# sample.voice.gateway.for.watson

This repository contains various samples and scripts to help you get started with the IBM&reg; Voice Gateway&trade;.

IBM&reg; Voice Gateway&trade; provides a Session Initiation Protocol (SIP) endpoint that orchestrates IBM&reg; Watson speech and Conversation services to enable a cognitive agent that can communicate with a caller using natural language. The voice gateway makes it possible to integrate a public or enterprise telephony system with Watson, enabling direct voice interactions with a cognitive self-service agent or the ability to run real-time analytics on a phone call between two people (e.g.  a customer and a contact center agent).

![](https://raw.githubusercontent.com/WASdev/sample.voice.gateway.for.watson/master/images/vgw-flow.png)

Within this repository you will find the following directories:

| Directory | Description |
| -------------- | --------------------------------------------------------------- |
| **\docker** | Contains sample **docker-compose.yml** files that can be used to launch the voice gateway docker images in your own docker environment.| 
| **\bluemix** | Contains scripts and **docker.env** files that can be used to deploy the voice gateway to the IBM&reg; Containers for Bluemix&reg; service.| 
| **\conversation** | Contains sample **docker-compose.yml** files that can be used to launch the voice gateway docker images in your own docker environment.| 
| **\kubernetes** | Contains contains scripts to help you get started with deployments of the voice gateway into a k8s environment.| 

### Pulling the IBM Voice Gateway Docker images
The voice gateway is made up of two separate Docker images that can be pulled using the following command:

 ```
 docker pull ibmcom/voice-gateway-so:latest

 docker pull ibmcom/voice-gateway-mr:latest
  ```

### Usage
All the documentation related to the Voice Gateway for Watson and the use of the files in this GitHub repository can be found here:

[Voice Gateway for Watson Documentation](https://cjcarpen.gitbooks.io/voice-gateway-for-watson/content/)

### Licenses
The license related to the files found in this GitHub repository:

[Apache 2.0 License](https://github.com/WASdev/sample.voice.gateway.for.watson/blob/master/LICENSE)

The license for the products installed within the IBM&reg; WebSphere&reg; Connect Voice Gateway for Watson&trade; Docker images can be found here:

[Voice Gateway for Watson License](https://raw.githubusercontent.com/WASdev/gitbook.voice.gateway.for.watson/master/la-license/LA_en.txt)
