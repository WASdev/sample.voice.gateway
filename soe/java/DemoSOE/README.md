Java based Service Orchestration Engine sample (SOE)

Java based Voice Proxy for integrating Voice Gateway for Watson, Watson Conversation Service and a clients backend APIs.
Banking Example

Purpose

The purpose of this project is to show how a developer can integrate the Watson Conversation service with the voice gateway in a more realistic way. A way that is more common in a clients environment either for a proof of concept or a production implementation. This demo focuses on a banking example, where the caller can ask about account balances and perform basic credit card actions on a sample database of user profiles.

Background

By default the IBM Voice Gateway (VGW) can communicate with the Watson Conversation Service (WCS) by using the REST services provided by the WCS. The service uses a single REST API for all conversation interactions. VGW exploits this API by creating the appropriate JSON payload when transcribing the spoken words from the caller and invoking the API. The challenge with VGW communicating directly with WCS is that there is no way to personalize the conversation interactions. WCS only maintains static information based on any one particular question being asked. If there is a desire to have dynamic responses, there needs to be a way for the runtime to make API calls to other services to lookup the additional information and provide it as part the response to either WCS or to VGW. This is where the voice proxy idea comes in.

Since WCS only has one API for the conversation, it is very easy to impersonate (proxy) that API. Also since the JSON format used in WCS is well documented, it is easy to ensure that the proxy can make updates and communicate with WCS on behalf of any invoker. VGW being the most interesting.

Goal

The goal of this sample is for the user to get an understanding of how to create a Proxy that communicates with both VGW and WCS. You can leverage this code or you can see the high level flow and create your own if Java isn't your thing. Some might prefer Node.JS, Python or even Node-Red.

Sample Watson Conversation Workspace

We have provided a sample Conversation Workspace as a part of the tutorial. The JSON is in the workspace folder. The sample workspace is a typical call center like scenario for banking.

We have 3 Entities define as part of the tutorial.

    Loans (Auto loan, Mortgage and Student Loan)
    Accounts (Checking, Savings and Money Market)
    Credit Card

We have defined four intents. When you open the workspace you can see what they are. But at a high level the following intents are available:

    Information: General information on the loans or accounts
    Balance: Check the balance of an account or a loan
    Payment: Make a payment on a loan from one of the accounts
    Activation: Activate a credit card


How to get this project working

Pre-requisites

The base assumption is you are using the IBM Voice Gateway and want to add dynamic responses based on the dialog from Watson Conversation Service. Also, we will assume you already have the IBM Voice Gateway installed and are ready to connect it to a WCS instance. There are several pieces of information needed for this tutorial.

1. Clone the repo
When pulling this project using eclipse, make sure to check the "Import Existing Projects" button during the clone
In order to get the maven dependencies. Right click on the Project and click Maven->Update Project. Inside the wizard, leave the defaults and hit OK. If maven still gives errors, try deleting the .m2 folder under your user profile on your machine and running Maven->Update Project while making sure to check the box for "Update Snapshots/releases"

2. A Liberty Server (Either locally or running on Bluemix)
Developing and Deploying using Eclipse

IBM® Eclipse Tools for Bluemix® provides plug-ins that can be installed into an existing Eclipse environment to assist in integrating the developer's integrated development environment (IDE) with Bluemix.
Download and install  IBM Eclipse Tools for Bluemix.
Import this sample into Eclipse using File -> Import -> Maven -> Existing Maven Projects option.
This project contains a simple servlet application.

3. Watson Conversation Credentials

Create an instance of Watson Conversation Service. Once the workspace has been created you need to import a new workspace. In the webcontent/workspace folder in the voiceProxy project, you will see a file voiceProxy-demo.json. Import this file into your workspace. This will create a new Conversation called VoiceProxy-Demo. This is the conversation you will be connecting to from the VoiceProxy Server.

Now we need to get access to the credentials for later use. Click on view credentials
Next we need to copy the workspace_id for use later

You are going to use the workspace ID above in the next step, along with the userid and password from the credentials page.

Conversation Workspace ID (You get this from your BlueMix Dashboard for the Conversation Service)
Userid to connect to the Conversation Service (You get this from your BlueMix Dashboard for the Conversation Service)
Password to connect to the Conversation Service (You get this from your BlueMix Dashboard for the Conversation Service)

Create a Liberty server definition:

In the Servers view in Eclipse right-click -> New -> Server
Select IBM -> WebSphere Application Server Liberty
Choose Install from an archive or a repository
Enter a destination path (/Users/username/liberty)
Choose WAS Liberty with Java EE 7 Web Profile
Continue the wizard with default options to Finish


Running the application using the command-line
This project can be built with Apache Maven. The project uses Liberty Maven Plug-in to automatically download and install Liberty from the Liberty repository. Liberty Maven Plug-in is also used to create, configure, and run the application on the Liberty server.
Use the following steps to run the application locally:
Execute full Maven build to create the target/DemoSOE.war file:
$ mvn clean install

Download and install Liberty, then use it to run the built application from step 1:
$ mvn liberty:run-server
Once the server is running, the application will be available under http://localhost:9080/DemoSOE. (Or whatever path your server is attached to)

4. Update server.env
Place the following environment variables in the server.env file for the Liberty server
    CONVERSATION_WORKSPACE_ID=[WORKSPACE ID FROM BLUEMIX]
    CONVERSATION_VERSION=2016-07-11
    CONVERSATION_USERNAME=[CONVERSATION SERVICE USERNAME FROM BLUEMIX]
    CONVERSATION_PASSWORD=[CONVERSTAION SERVICE PASSWORD FROM BLUEMIX]

5. Update Docker-Compose
Now you need to change the docker-compose.yml file from the IBM Voice Gateway. Since the default with the Voice Gateway is to talk directly to the Conversation Service, you need to change the parameter WATSON_CONVERSATION_URL to point to the voiceProxyServer IP address. You need to change it to the IP of where the voiceProxyServer is running. In addition you need to specify the port the server is listening on. The default is 5000. The url will be the one provided when the liberty server is started. However the /rest must be added to the end of the liberty server url.
    WATSON_CONVERSATION_URL=http://localhost:9147/SOE/rest
    **Note the /rest is necessary at the end of the liberty server url

In this example the port the VoiceProxyServer is listening on is 9147 running on server SERVER_NAME

6. Run Server
You can now start the server by starting the server in eclipse. You should see something like the following
[AUDIT   ] CWWKE0001I: The server (SERVER_NAME) has been launched.
[AUDIT   ] CWWKE0100I: This product is licensed for development, and limited production use. The full license terms can be viewed here: https://public.dhe.ibm.com/ibmdl/export/pub/software/websphere/wasdev/license/base_ilan/ilan/17.0.0.1/lafiles/en.html
[AUDIT   ] CWWKZ0058I: Monitoring dropins for applications.
[AUDIT   ] CWWKT0016I: Web application available (default_host): http://localhost:9147/SOE/

Run your application locally on Liberty:

Create the war file by running:
mvn package
This will create a Demo-SOE snapshot file in the target directory of the project.  Add this file to the dropins folder of the liberty server. 

Run your application on Bluemix:

Right click on the JavaHelloWorldApp sample and select Run As -> Run on Server option
Find and select the IBM Bluemix and press Finish
A wizard will guide you with the deployment options. Be sure to choose a unique Name for your application
In a few minutes, your application should be running at the URL you chose.

7. The user can now call into Voice Gateway normally and the call will be sent through the SOE.

Voice Script

In an effort to help with using the demo it would be beneficial to know what questions to ask WCS. Below are the sample questions. Remember, there is an API that keeps track of the balances, so if you withdraw too much money you will get errors.

Conversation Flow 1

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

Conversation Flow 2
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
