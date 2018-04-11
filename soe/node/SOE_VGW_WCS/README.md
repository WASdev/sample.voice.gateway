

# SOE-VGW-WCS
This code is developed to illustrate how Service Orchestration Engine (SOE) can be implemented for IBM Voice Gateway (VGW).
This code connects the VGW to a Watson Conversation Service (WCS), with intermediate actions.  


## Usage
This code is a startup code towards implementing SOE for IBM Voice Gateway in NodeJS.


## Developing
This code does the following actions:
1) Gets input from IBM Voice Gateway (STT).
2) Passes on the input to WCS.
3) Gets response from WCS.
4) Add TTS customization tags to the response
5) Add Voice Gateway customization tags to the response.
6) Trigger mail if intents detected.
7) Send back output to IBM Voice Gateway (TTS)  


### Tools

