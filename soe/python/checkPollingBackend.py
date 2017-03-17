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
from voiceProxyUtilities import startPolling, stopPolling, inPollingState, earlyReturn


logging_comp_name = "checkPollingBackend"


voiceProxySettings.POLLING_URL = ''
	
def pollBackend(message):
	message = preCheckPollingBackend(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'preCheckPollingBackend -> Returning to Gateway', message)
		return message


	message = checkPollingBackend(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'checkPollingBackend -> Returning to Gateway', message)
		return message

	message = postCheckPollingBackend(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'postCheckPollingBackend -> Returning to Gateway', message)
		return message
		
	return message



def preCheckPollingBackend(message):
	return message

def checkPollingBackend(message):
	return message

def postCheckPollingBackend(message):
	return message


def checkPollingAfterConversation(message):
	return message	







def pollingSubProcess(message):
	return message

	



#------------ Polling Helper Methods --------------
# Because we are talking to the Chat SOE, we need to 
# see if we need to poll and send a message back to the user about waiting			

def needStartPolling(message):
	return False


def continuePolling(message):
	return False


def hasOutputText(message):
	if 'output' in message:
		if 'text' in message['output']:
			if len(message['output']['text']) > 0:
				logging.info('hasoutputtext is true')
				return True
			else:
				return False
		else:
			return False
	else:
		return False

def setEarlyReturn(message, logmessage):
	message['context']['cisContext']['earlyReturn'] = True
	message['context']['cisContext']['earlyReturnMsg'] = logmessage
	
	return message

def poll(message):
	POST_SUCCESS = 200
	url = settings.POLLING_URL
	r = requests.post(url, auth=(voiceProxySettings.POLLING_USERNAME, voiceProxySettings.POLLING_PASSWORD), headers={'content-type': 'application/json'}, data=json.dumps(message))
	if r.status_code == POST_SUCCESS:
		message = r.json()
	return message
#-------------- End Polling Helper Methods ------------------		