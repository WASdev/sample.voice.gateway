

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


## Dependencies

This application requires one service instance of IBM Voice Gateway.
IBM Voice Gateway in turn requires one Watson Assistant (former Watson Conversation), one Watson Speech To Text, and one Watson Text To Speech Service instance.
Combined, the above four services has to be running to demonstrate/run this application.

## Parameters

Please set the following parameters in the manifest.yml file.

wcs_username: This is the username for the Watson Assistant (former Watson Conversation) service
wcs_password: This is the password for the Watson Assistant (former Watson Conversation) service
wcs_workspace: This is the workspace identifier for the Watson Assistant (former Watson Conversation) service
show_all_logs: Boolean, either true or false
receiver_email_address: Some email address, comma separated multiple email addresses permitted
sender_email_address: Some email address, only one permitted
sender_email_password: Password for the sender email address

These parameters would get uploaded as environment variables for the bluemix application.
The parameters can also be modified at the runtime from the environment variables configuration page of the bluemix application.

## Deploying the Application Locally

This application is designed to be runnable in a blueminx NodeJS container, and running locally is not recommended.
Still, for testing out locally, the reference to the above environment variables within the app.js code has to be replaced with exact values.
Subsequently, the app.js file should be run using NodeJS command.

## Deploying the Application on Bluemix (IBM Cloud)

Change the name and host of the application in the manifest.yml file. They should be unique in the cloud.
Make sure either cloudfoundry command line interface (cf-cli) or bluemix command line interface (bluemix-cli) is installed in the machine.
Connection to IBM cloud and login/authentication done through the CLI.
From the project root directory, execute either of the following, depending on the CLI used.
cf push
bluemix app push <app_name> -m 512m
More references can be found at https://console.bluemix.net/docs/runtimes/nodejs/getting-started.html#getting-started-tutorial and https://console.bluemix.net/docs/starters/upload_app.html

## Post Deployment Configuration

After deployment, the base URL of the running application can be obtained from the application home page on bluemix platform.
The REST endpoint to the application's API is POST : <base_url>/callSOE
This REST API endpoint has to be provided to the service orchestration engine configuration section of the IBM Voice Gateway Service instance.
More reference can be found at https://www.ibm.com/support/knowledgecenter/en/SS4U29/serviceorchestration.html


