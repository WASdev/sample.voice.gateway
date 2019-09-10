# Python based Service Orchestration Engine sample (VoiceProxy)
Python based Voice Proxy for integrating Voice Gateway for Watson, Watson Conversation Service and a clients backend APIs.

## Purpose
The purpose of this project is to show how a developer can integrate the Watson Conversation service with the voice gateway
in a more realistic way. A way that is more common in a clients environment either for a proof of concept or a production
implementation. 

## Some Background
By default the IBM Voice Gateway (VGW) can communicate with the Watson Conversation Service (WCS) by using the REST
services provided by the WCS. The service uses a single REST API for all conversation interactions. VGW exploits this API by
creating the appropriate JSON payload when transcribing the spoken words from the caller and invoking the API. The challenge with
VGW communicating directly with WCS is that there is no way to personalize the conversation interactions. WCS only maintains static
information based on any one particular question being asked. If there is a desire to have dynamic responses, there needs to be
a way for the runtime to make API calls to other services to lookup the additional information and provide it as part the response
to either WCS or to VGW. This is where the voice proxy idea comes in. 

Since WCS only has one API for the conversation, it is very easy to impersonate (proxy) that API. Also since the JSON format
used in WCS is well documented, it is easy to ensure that the proxy can make updates and communicate with WCS on behalf of any
invoker. VGW being the most interesting.

## Goal
The goal of this sample is for the user to get an understanding of how to create a Proxy that communicates with both VGW and WCS. Additionally for the user to get an appreciation for some of the common aspects that exists (patterns) when the proxy is being used. These patterns
are based on several client implementations. In essence lessons learned. You can leverage this code or you can see the high level flow and create your own if python isn't your thing. Some might prefer Node.JS, Java or even Node-Red.

## Sample Watson Conversation Workspace
We have provided a sample Conversation Workspace as a part of the tutorial. The JSON is in the workspace folder. The sample 
workspace is a typical call center like scenario for banking. 

We have three Entities define as part of the tutorial.

1. Loans (Auto loan, Mortgage and Student Loan)
2. Accounts (Checking, Savings and Money Market)
3. Credit Card

We have defined four intents. When you open the workspace you can see what they are. But at a high level the
following intents are available:

1. Information: General information on the loans or accounts
2. Balance: Check the balance of an account or a loan
3. Payment: Make a payment on a loan from one of the accounts
4. Activation: Activate a credit card


## Getting Started
Getting started is very simple. Once the code has be cloned, you can deploy the code locally or on IBM's BlueMix. 
Instructions for both approaches are provided below.


### Pre-requisites
The base assumption is you are using the IBM Voice Gateway and want to add dynamic responses based on the dialog
from Watson Conversation Service. Also, we will assume you already have the IBM Voice Gateway installed and are ready to connect
it to a WCS instance. There are several pieces of information needed for this tutorial.

1. Conversation Workspace ID (You get this from your BlueMix Dashboard for the Conversation Service)
2. Userid to connect to the Conversation Service (You get this from your BlueMix Dashboard for the Conversation Service)
3. Password to connect to the Conversation Service (You get this from your BlueMix Dashboard for the Conversation Service)
4. URL of your VoiceProxy application (More on this in a few minutes)
5. Python version 2.7.12 if running standalone
6. Python Flask application if running in BlueMix
7. CloudantDB for Web logging (_optional feature_)


### Local Deployment
Below are the steps to get started with the sample application for local deployment
Once you have checked the code out you need to make a couple of updates

1. You need to install the following python package.  
  You can cut and paste each item below on a command line   
  `pip install requests`   
  `pip install flask`   
  `pip install xmltodict`   
  `pip install couchdbkit`   

   The above only take a few minutes
   
2. Create an instance of Watson Conversation Service. Once the workspace has been created you need to 
import a new workspace. In the workspace folder in the voiceProxy project, you will see a file voiceProxy-demo.json.
Import this file into your workspace. This will create a new Conversation called VoiceProxy-Demo. This is the convesation
you will be connecting to from the VoiceProxy Server.   

	![Image of conversation tile](./images/Watson-Conversation-tile.png)   
	
	Create your new conversation service. 
   
   ![Image of conversation service ](./images/Watson-conversation-create-service.png)
	
	From the source code under the **workspace** folder is a JSON file voiceProxy-demo.json. You need to import this file into your workspace.
	
	Now we need to get access to the credentials for later use. Click on view credentials
	
	![Image of conversation credentials ](./images/Watson-conversation-credentials.png)
	
	Next we need to copy the workspace_id for use later
	
	![Image of conversation workspace  ](./images/Watson-conversation-wks-id.png)
	
   You are going to use the workspace ID above in the next step, along with the userid and password from the credentials page.   
   

3. Export the following environment variables
	- CONVERSATION_WORKSPACE_ID=**workspaceid**
	- CONVERSATION_VERSION=**2016-07-11**
	- CONVERSATION_USERNAME=**username**
	- CONVERSATION_PASSWORD=**password**
	- CONVERSATION_URL=https://gateway.watsonplatform.net/conversation/api

	If you are going to enable web logging you need to also update the following variables:
	- WEB_LOGGING=True
	- CLOUDANT_URL='you cloudant apr URL'
  
4. Now you need to change the docker-compose.yml file from the IBM Voice Gateway. Since the default with the Voice
Gateway is to talk directly to the Conversation Service, you need to change the parameter WATSON_CONVERSATION_URL to point
to the voiceProxyServer IP address. You need to change it to the IP of where the voiceProxyServer is running. In addition you
need to specify the port the server is listening on. The default is 5000. Example is below.   
   - WATSON_CONVERSATION_URL=http://10.2.2.31:5000   
   
   In this example the machines IP address is 10.2.2.31 and the port the VoiceProxyServer is listening on is 5000

5. You can now start the server by typing "python voiceProxyServer.py"
You should see something like the following
2017-03-17 05:01:52,372 - INFO -  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)



We will supply a link to another project where you can get a viewer for the log entries stored in cloudantDB.  

### BlueMix Deployment
If you want to deploy the application to BlueMix the steps are very straight forward.

1. Create an instance of Watson Conversation Service. Once the workspace has been created you need to 
import a new workspace. In the workspace folder in the voiceProxy project, you will see a file voiceProxy-demo.json.
Import this file into your workspace. This will create a new Conversation called VoiceProxy-Demo. This is the convesation
you will be connecting to from the VoiceProxy Server. 

	![Image of conversation tile](./images/Watson-Conversation-tile.png)
	
	Create your new conversation service. 
	
	![Image of conversation service ](./images/Watson-conversation-create-service.png)
	
	From the source code under the **workspace** folder is a JSON file voiceProxy-demo.json. You need to import this file into your workspace.

	Now we need to get access to the credentials for later use. Click on view credentials
	
	![Image of conversation credentials ](./images/Watson-conversation-credentials.png)
	
	Next we need to copy the workspace_id for use later
	
	![Image of conversation workspace  ](./images/Watson-conversation-wks-id.png)
	
	
2. Create a new Python Flask application on BlueMix. Keep track of you application and host names, you will need it later.

	![Image of Bluemix](./images/python-flask-tile.png)
	
	![Image of Create Bluemix app](./images/python-flask-create-app.png)
	
3. Go to the command line where you cloned the source code from GitHub.
Login to BlueMix from the command line, from within the voiceProxyServer directory
`cf login -a na.api.bluemix.net`   
	
	#### Update Manifest
	
	Update the supplied manifest.yml from the source code you cloned for the voiceProxyServer.
	You need to ensure the values for the following have been updated with your unique values.
	
	- Name="name from your Python application"
	- Host="host name from Python application"
	- CONVERSATION_WORKSPACE_ID=**workspaceid**
	- CONVERSATION_VERSION=**2016-07-11**
	- CONVERSATION_USERNAME=**username**
	- CONVERSATION_PASSWORD=**password**
	- CONVERSATION_URL=https://gateway.watsonplatform.net/conversation/api

	If you are going to enable web logging you need to also update the following variables:
	- WEB_LOGGING: True
	- CLOUDANT_URL: 'you cloudant apr URL'   
	By updating the manifest.yml file, bluemix will automatically add the appriopriate environment variables to the application. You will want to double check they have been added. There is a step below to do that.

	#### Push changes
	
	Once you changed the manifest.yml and you are logged on to Bluemix, issue the following command to push the voiceProxyServer to BlueMix
	
	`cf push YourApplication Name From Step 2`
	
	BlueMix will use the configuration defined and add all the appropriate dependencies. 
	Sometimes, the application will not start the first time. This seems to be a bug in Bluemix. I recommend
	issuing the push command again. It seems to work the second time.
	![command line](./images/bluemix-command-line.png)


5. On BlueMix, make sure the following environment variables have been added to the application. These can be checked
 by clicking on the **Runtime** menu item on the left. 
Then in the center of the screen there is an option for **Environment Variables**. 
Click on the link and then add your values where appropriate and then click on the **Save** button.   
Your screen should look like below:   
![Image of Python add Env Vars  ](./images/python-flask-environment-vars-filled.png)   

6. Now you need to change the docker-compose.yml file from the IBM Voice Gateway. Since the default with the Voice
Gateway is to talk directly to the Conversation Service, you need to change the following parameter:   

   - WATSON_CONVERSATION_URL
   to the voiceProxyServer IP address. You need to change it to the IP or the hostname of where the voiceProxyServer is running. In addition you 
   need to specify the port the server is listening on, if you change from the default of 80, defined by Bluemix.   

   
   In this example we are using the route defined from your BlueMix application you created in step 1. Because bluemix handels the ports for you, you don't need to make any other port changes.   
   - WATSON_CONVERSATION_URL=https://pythonbluemixapplication 

   You can now restart the Voice Gateway Docker containers by issuing the following command:   
   `docker-compose up`  

## Voice Script
In an effort to help with using the demo it would be beneficial to know what questions to ask WCS. Below are the sample
questions. Remember, there is an API that keeps track of the balances, so if you withdraw too much money you will get errors. 
You can try the questions by calling into the voice gateway or try with a simple web client special for the voiceProxyServer, 
which is included in the voiceProxyServer runtime. See next sections.

Conversation script for Accessing User Profile Data
1. I would like to pay my mortgage
2. My name is Brian
3. Yes it is
4. baseball
5. I want to use my checking account
6. I want to pay two hundred dollars
7. Thank you
8. What is the balance of my checking account
9. Thank you.
10. Good-bye

Conversation script for using DTMF collection
1. I would like to add a credit card
2. My name is Olivia
3. yes
4. gymnastics
5. mastercard
6. [type in card number]

### Simple Web Client Testing
Once the Proxy has been deployed, you can test it by using the a built in Web Client. You can access the web client by using the following url: ***https://url-of-proxy/webclient***   

You should see a screen similar to the following, but without the text:   

![cloudant query](./images/webclient_example.png)

### Setup of WebLogging Tool

If you want to use the WebLogger to keep track of log events in the voiceProxyServer for the conversation flows between the IBM Voice Gateway and WCS
you need to provision a cloudantDB instance. By default the WebLogger is turned off. But you might want to enable it
for debugging purposes. You can install cloudantDB  on BlueMix for free. If you want to use the WebLogger you need to
do the following:

1. **export CLOUDANT_URL = someurl** (This is an environment variable for BluxMix deployments) 
The URL is on the "Services Credentials" tab in your cloudant dashboad on BlueMix. Click the "View Credentials" button to see the credentials. URL should be on the bottom.

2. **export WEB_LOGGING = True**   (This is an environment variable for BluxMix deployments)


3. Update your CloudantDB information by logging into cloudant and by doing the following steps:
     1. Create a new database called **soelogging**
     ![cloudant create database](./images/cloudant-create-db.png)

     2. Create new Design Document, document view 
     ![cloudant create view](./images/cloudant-create-view.png)
     
     3.  Call it **"logEntry"** and then click the "Create Document and Build Index" button
     ![cloudant create logEntry](./images/cloudant-create-view-logentry.png)
     
     
     4.  Now edit the logEntry document by clicking on database button and then All Documents. Your newly created view "logEntry" should be the only document in the list. Click on the upper right corner of the document "pencil icon" to edit the document.
     ![cloudant edit logEntry](./images/cloudant-update-logentry.png) 

     5. Copy the text from the bottom of this section and paste it into the document, overwriting everything except the "id" and "rev" lines. Make sure to paste right after the 'comma' at the end of the "rev" line.


```JSON	
	"views": {
	"comments": {
	  "map": "function (doc) {\n  if(doc.comment){\n   emit(doc.comment, [doc.sessionID,doc.conversationid]);\n  }\n}"
	},
	"sessionID": {
	  "map": "function (doc) {\n  if(doc.sessionID){\n    emit(doc.sessionID, [doc.sessionID,doc.application]);\n  }\n}"
	},
	"application": {
	  "map": "function (doc) {\n  if(doc.application){\n    emit(doc.application, 1);\n  }\n}"
	},
	"uniqueSessions": {
	  "map": "function (doc) {\n  emit(doc.sessionID, [doc.sessionID,doc.application]);\n}",
	  "reduce": "function (keys, values, rereduce) {\n  return(keys,null)\n}"
	}
	},
	"language": "javascript",
	"indexes": {
	"fullIndex": {
	  "analyzer": "standard",
	  "index": "function (doc) {\n  if(doc.sessionID){\n    index(\"sessionID\", doc.sessionID,{\"store\": true});\n  }\n  if(doc.conversationid){\n    index(\"conversationid\", doc.conversationid,{\"store\": true});\n  }\n  if(doc.logtime){\n    index(\"logtime\", doc.logtime,{\"store\": true});\n    }\n  if(doc.component){\n    index(\"component\",doc.component,{\"store\": true});\n  }\n  if(doc.comment){\n    index(\"comment\", doc.comment,{\"store\": true});\n  }\n  if(doc.msg_input_text){\n    index(\"msgInputText\",doc.msg_input_text,{\"store\": true});\n  }\n  if(doc.msg_output_text){\n    index(\"msgOutputText\",doc.msg_output_text,{\"store\": true});\n  }\n}"
	},
	"logTime": {
	  "analyzer": "standard",
	  "index": "function (doc) {\n  if(doc.logtime){\n    index(\"logtime\", doc.logtime);\n  }\n}"
	}
	}
```
     

![cloudant logEntry paste](./images/cloudant-logentry-paste.png)

Your screen should now have some new search indexes and views.
![cloudant logEntry paste](./images/cloudant-logentry-updated.png)


4. Create new query documents and Indexes.
	1. Now you need to create query indexes for your web queries. Click on the "Query" button. Then click the **edit** button to the right of "Queryable Indexes" label.
	![cloudant query](./images/cloudant-query-index.png)

	8. You should now see the following screen
	![cloudant query index ](./images/cloudant-query-index-create.png)

	9. Paste the following into the little editor window, overwriting the existing text. This creates an index for the sessionID attribute. Then click the create index button.
You should now see two documents on the right side of the screen. The "special_id" and "JSON sessionID".

```JSON
     {
     "index": {
        "fields": ["sessionID"]
    },
    "type" : "json"
	}
```

![cloudant query](./images/cloudant-query-index-create-sessionid.png)
Paste the following into the editor, overwriting the existing text. This now creates an index for the logtime attribute. Then click the create index button.

```JSON
     {
    "index": {
        "fields": ["logtime"]
    },
    "type" : "json"
}
```
![cloudant query](./images/cloudant-query-index-create-logtime.png)
Paste the following into the editor, overwriting the existing text. This now creates an index for the both the logtime and sessionid attributes. Then click the create index button.

```JSON
{
    "index": {
        "fields": ["logtime","sessionID"]
    },
    "type" : "json"
}
```
![cloudant query](./images/cloudant-query-index-create-logtime-sessionid.png)
Finally, your screen should look like the following
![cloudant query](./images/cloudant-query-index-create-completed.png)

Your database is now set up to add new log entries and then query them to see how the conversation flows between the Watson Voice Gateway and Watson Conversation Service

To access the webLogging tool you can point your browser to the url of the proxy application:   
***https://url-of-proxy/soeLogging***

You will see a screen like the following:
![seologging](./images/soe-weblogging.png)
You will need a the sessionID from a call to the Watson Voice Gateway. The sessionID is used as the unique key. Once a sessionID is provide hit search. You should now a a list of conversation log enties. You can click on one of the entries to see the JSON for that point in time.
![seologging](./images/soe-weblogging-example.png)

Thas is is, you are fully running with logging enabled. Remember this is for debugging and not for production use. The intent is to help identify the flow of the data from the Watson Voice Gateway and Watson Conversation Service. If you run too many logs, Cloudant DB will complain because there are too many write requests per second.

## REST API's

If you want to turn the WebLogging on and off during runtime, you can invoke an API and pass a JSON object to turn the logging on or off.
URL for the API to make changes to the state variables is accessed by the following URL:   
### API LOGGING State
GET to https://url-of-proxy/cis/weblogging 
response should look something like:  
```JSON
{
    "cisContext": {
        "cisCustomerWait": false,
        "cisBargein": false,
        "cisDTMF": {
            "enabled": false,
            "localDictonary": true
        },
        "cisWebLogging": true,
        "cisPolling": {
            "password": "",
            "URL": "",
            "sleepTime": 10,
            "username": ""
        }
    }
}
```

### API LOGGGING ON

PUT to https://url-of-proxy/cis/weblogging   

```JSON
{"cisContext":
{"cisWebLogging": true }

}
```
### API LOGGGING OFF
PUT to  https://url-of-proxy/cis/weblogging   

```JSON
{"cisContext":
{"cisWebLogging": false }

}
```
The response from the PUT will be a JSON object with the current variable state.
 
