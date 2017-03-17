# Service Orchestration Engine (SOE) samples 
-------------------
The Service Orchestration Engine (SOE) provides a simple way to customize the behavior of the IBM Voice Gateway. It acts as a Watson Conversation proxy that sits between the IBM Voice Gateway and the Watson Conversation service, modifying request sent from the voice gateway to Watson and modifying responses sent back to the voice gateway from Watson:

![](https://raw.githubusercontent.com/WASdev/sample.voice.gateway/develop/images/soe.png)

Most production deployments of the IBM Voice Gateway will need an SOE for the following reasons:

 - De-identification of Watson Conversation requests
 - Personalize the Watson Conversation responses
 - Use telephony features like Caller-id, DTMF, etc.
 - Integrate with API’s to enhance the user interaction
 - Exploit Voice Gateway features using state variables 
 - Voice security integration using DTMF or biometrics

In this directory you will find samples for the SOE written in various languages. Currently, there is a Python example but we hope to follow it up with samples written in JavaScript for Nodejs and Java.
