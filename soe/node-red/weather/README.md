# Weather Voice Agent SOE sample built with Node-RED

This sample shows how to build a Service Orchestration Engine for Voice Gateway using Node-RED. Node-RED is a programming tool for wiring together 
hardware devices, APIs and online services on top of Node.js. For more details go to: https://nodered.org/

This very simple sample shows how to create a voice agent that converts a city and state captured from the caller into a current day weather forecast. It relies
on the Watson Conversation Node-RED node and the Weather Insights Node-RED node to simplify the creation of the flow. 

To quickly setup this sample follow these steps:

1. Create the following Bluemix services: [Watson Speech To Text](https://console.bluemix.net/catalog/services/speech-to-text), 
[Watson Text To Speech](https://console.bluemix.net/catalog/services/text-to-speech), 
[Watson Assistant](https://console.bluemix.net/catalog/services/watson-assistant-formerly-conversation), 
[Weather Company Data](https://console.bluemix.net/catalog/services/weather-company-data) service and 
the new [IBM Voice Agent with Watson](https://console.bluemix.net/catalog/services/voice-agent-with-watson) service.
1. Create a Twilio SIP trunk, assign a phone number to it and point it at the IBM Voice Agent with Watson service.
1. Create a Node-RED server in Bluemix and import the **vgw-weather-node-red-flow.txt** file.
1. Create the Watson Conversation workspace using the **vgw-conversation-flow.json** file.
1. Configure the Assistant node and the Weather Insights node to point to your associated Bluemix services.
1. Modify the username and password fields in the URL in the **Geo Lookup** function node to match your Weather Insights service.
1. Setup a Voice Agent in the IBM Voice Agent with Watson service with the phone number provisioned in step 1. 
1. You'll also need to point your voice agent at your SOE.

In terms of the Voice Gateway interactions, this SOE demo is extremely simple. The only complexity comes from the fact that two request to The Weather Service are 
required to get the daily forecast. The first request converts the city and state names into a longitude and latitude which is required to get the daily forecast. 
The second request to The Weather Service retrieves the daily forecast. Note that during these request to The Weather Service, the Voice Gateway payload is 
preserved in a msg variable called **vgwPayload**. This must be preserved so that the response that goes back to the VGW has all the payload from Conversation plus any 
changes made by the SOE to the output text.

Please comment on the public Slack channel if you run into any issues or feel these instructions are somehow lacking.

