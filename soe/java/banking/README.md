# Java based Service Orchestration Engine sample (SOE)

Java based Voice Proxy for integrating Voice Gateway/Voice Agent with Watson, Watson Conversation Service and a clients backend APIs.
Banking Example

## Purpose

The purpose of this project is to show how a developer can integrate the Watson Conversation service with the Voice Gateway/Voice Agent with Watson in a more realistic way. A way that is more common in a clients environment either for a proof of concept or a production implementation. This demo focuses on a banking example, where the caller can ask about account balances and perform basic credit card actions on a sample database of user profiles.

## Background

By default the IBM Voice Gateway (VGW)/Voice Agent with Watson (VAW) can communicate with the Watson Conversation Service (WCS) by using the REST services provided by the WCS. The service uses a single REST API for all conversation interactions. VGW/VAW exploits this API by creating the appropriate JSON payload when transcribing the spoken words from the caller and invoking the API. The challenge with VGW/VAW communicating directly with WCS is that there is no way to personalize the conversation interactions. WCS only maintains static information based on any one particular question being asked. If there is a desire to have dynamic responses, there needs to be a way for the runtime to make API calls to other services to lookup the additional information and provide it as part the response to either WCS or to VGW/VAW. This is where the service orchestration engine (SOE) comes in.

Since WCS only has one API for the conversation, it is very easy to impersonate (proxy) that API. Also since the JSON format used in WCS is well documented, it is easy to ensure that the proxy can make updates and communicate with WCS on behalf of any invoker. VGW being the most interesting.

## Goal

The goal of this sample is for the user to get an understanding of how to create an SOE that communicates with both VGW/VAW and WCS. You can leverage this code or you can see the high level flow and create your own if Java isn't your thing. Some might prefer Node.JS, Python or even Node-Red.

## Sample Watson Conversation Workspace

We have provided a sample Conversation Workspace as a part of the tutorial. The JSON is in the conversation_skill folder. The sample workspace is a typical call center like scenario for a banking service.

We have 3 Entities define as part of the tutorial.

1. Loans (Auto loan, Mortgage and Student Loan)
2. Accounts (Checking, Savings and Money Market)
3. Credit Card

We have defined four intents. When you open the workspace you can see what they are. But at a high level the following intents are available:

1. Information: General information on the loans or accounts
2. Balance: Check the balance of an account or a loan
3. Payment: Make a payment on a loan from one of the accounts
4. Activation: Activate a credit card


## How to start the sample

### Pre-requisites

* For running this SOE sample you must first have either an IBM Voice Gateway or Voice Agent with Watson deployment set up with all the credentials for Text, Speech and Speech to Text.

* In your Watson Assistant workspace create an agent or use an existing agent and create a new skill with the json configuration in the conversation_skill folder

* If you're using Voice Agent fill in the credentials used in Watson Assistant with the values for the skill created in the previous step except the conversation url which will point to our SOE. If you're using Voice Gateway you only need to specify the conversation url which will point to our SOE

* You're ready to start running the sample!

### Starting SOE

**For running this sample you need java and maven installed on your machine**

#### Quick deployment

Using the maven Open liberty plugin you can quickly start the application as is
1. Clone the project to your machine and in a teminal window change directory to this sample

2. In the src/main/wlp directory modify the server.env to include the credentials needed for connecting to Watson Assistant

```
WORKSPACE_ID=Newly created workspace id
CONVERSATION_VERSION=2016-07-11
CONVERSATION_USERNAME=Username for connecting to watson assistant. If you're using an apikey fill this with "apikey"
CONVERSATION_PASSWORD=Password for connecting to watson assistant. If you're using an apikey fill this with the value of the apikey
CONVERSATION_URL=Url for connecting to the Watson Assistant API
```

3. On the terminal window run `mvn clean package liberty:run` and this will start the SOE. It has an http port of 9080 and an https port of 9443 by default. You can change these in the pom.xml of the project in the properties section `testServerHttpPort` and `testServerHttpsPort`.

4. Your SOE sample should be running now! 

**Important:** In Voice Gateway configuration set the WATSON_CONVERSATION_URL to the URL of the sample that just started. In Voice Agent setup your agent to use a Service Ochestration Engine and set the URL to the URL of the sample that just started. The URL is: `{protocol}://{host}:{port}/banking/rest/bankWebhook` change the placeholders to fit your sample but remember to end the URL with **/banking/rest/bankWebhook**

#### Build this project from source and play around with it

1. Clone the project to your machine and in a teminal window change directory to this sample.

2. You can import this project as a maven project in eclipse for modifying the sample

3. Create a Liberty server with the server.xml included in the src/main/wlp directory and in the server.env of that server include and fill the credentials necessary for connecting to Watson Assistant

```
WORKSPACE_ID=Newly created workspace id
CONVERSATION_VERSION=2016-07-11
CONVERSATION_USERNAME=Username for connecting to watson assistant. If you're using an apikey fill this with "apikey"
CONVERSATION_PASSWORD=Password for connecting to watson assistant. If you're using an apikey fill this with the value of the apikey
CONVERSATION_URL=Url for connecting to the Watson Assistant API
```

4. Package the app running in a terminal window `mvn clean package`

5. Move the packaged war app to the dropins of the server and start the server

6. Your SOE sample should be running now!


**Important:** In you Voice Gateway/Voice Agent configuration change the conversation url to the URL of the sample that just started which is: `{protocol}://{host}:{port}/banking/rest/bankWebhook` change the placeholders to fit your sample but remember to end the URL with **/banking/rest/bankWebhook**

### How it works

* All the data for the customer are stored in the src/main/webapp/WEB-INF/callerProfile.csv. The SOE acesses this data for getting the info and validating the customer information

* If the SOE recognizes an intent that applies to it, it will take a turn and get the information from the csv and include it for the conversation with Watson Assistant. If not, it will just forward requests to Watson Assistant without interfering.

# Voice Scripts

In an effort to help with using the demo it would be beneficial to know what questions to ask WCS. Below are the sample questions. Remember, there is an API that keeps track of the balances, so if you withdraw too much money you will get errors.

Conversation Flow 1:

Hi I am Watson. How can I help you today?
    "I would like to pay my mortgage"
I need some personal information. Please say your first name.
    "My name is Brian"
I have your first name as Brian, is that correct?
    "Yes it is"
Please clearly say our password.
   "baseball"
Okay you want to pay your mortgage. What account do you want to use?
    "I want to use my checking account"
We will use your checking account. How much would you like to pay?
    "I want to pay two hundred dollars"
Okay we will move $200 from your checking account. Is there anything else I can help with?

Conversation Flow 2:

Hi I am Watson. How can I help you today?
    "I want to add a credit card"
I need some personal information. Please say your first name.
    "Olivia"
I have your first name as Olivia, is that correct?
    "Yes"
Please clearly say our password
    "Gymnastics"
What type of card would you like to add?
    "Mastercard"
Please enter your card number
    (Input card number with keypad)
Okay I have added your card. Is there anything else I can help you with?
