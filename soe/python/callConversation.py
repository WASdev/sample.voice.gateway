# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
from weblogger import addLogEntry
import voiceProxySettings
from voiceProxyUtilities import setEarlyReturn, earlyReturn
import checkPollingBackend 

logging_comp_name = "callConversation"

CONVERSATION_URL = 'https://gateway.watsonplatform.net/conversation/api/v1/workspaces/'
CONVERSATION_SOE_URL = ''
SOE = False


#####
# Overwrites by env variables
#####
if 'CONVERSATION_WORKSPACE_ID' in os.environ:
	CONVERSATION_WORKSPACE_ID = os.environ['CONVERSATION_WORKSPACE_ID']
if 'CONVERSATION_USERNAME' in os.environ:
	CONVERSATION_USERNAME = os.environ['CONVERSATION_USERNAME']
if 'CONVERSATION_PASSWORD' in os.environ:
	CONVERSATION_PASSWORD = os.environ['CONVERSATION_PASSWORD']
if 'CONVERSATION_VERSION' in os.environ:
	CONVERSATION_VERSION = os.environ['CONVERSATION_VERSION']
if 'CONVERSATION_SOE' in os.environ:
	SOE = os.environ['CONVERSATION_SOE']
if 'CONVERSATION_SOE_URL' in os.environ:
	CONVERSATION_SOE_URL = os.environ['CONVERSATION_SOE_URL']
	


#------- Check SOR Before Conversation Methods -----------------

def callConversationService(message):
	message = preCallConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'preCallConversation -> Returning to Gateway', message)
		return message
	
	message = callConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'callConversation -> Returning to Gateway', message)
		return message
	
	
	
	# $$$$$$$ 
	message = fromConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'fromConversation -> Returning to Gateway', message)
		return message
		
	message = postCallConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'postCallConversation -> Returning to Gateway', message)
		return message
	
	message = checkPollingAfterConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'checkPollingAfterConversation -> Returning to Gateway', message)
		return message
		
	return message



def preCallConversation(message):
	return message

def fromConversation(message):
	return message
	
def callConversation(message):
		# talk to the conversation Service	
	addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, "Sent to Conversation", message)
	message = converse(message)
	addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, "Back from Conversation", message)

	return message

def postCallConversation(message):
	return message


def checkPollingAfterConversation(message):
	return checkPollingBackend.checkPollingAfterConversation(message)
	
#------ End Check SOR Before Conversation Methods ---------------


def converse(message):
	global CONVERSATION_WORKSPACE_ID, CONVERSATION_USERNAME, CONVERSATION_PASSWORD, CONVERSATION_VERSION
	POST_SUCCESS = 200
	url = ""
	if SOE:
		url = CONVERSATION_SOE_URL
	
	else:
		url = CONVERSATION_URL + CONVERSATION_WORKSPACE_ID + '/message?version=' + CONVERSATION_VERSION
	
	r = requests.post(url, auth=(CONVERSATION_USERNAME, CONVERSATION_PASSWORD), headers={'content-type': 'application/json'}, data=json.dumps(message))
	if r.status_code == POST_SUCCESS:
		message = r.json()
		
	return message