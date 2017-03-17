# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
from weblogger import addLogEntry

from voiceProxyUtilities import setEarlyReturn, earlyReturn, check_wcsActionSignal
from callConversation import callConversationService

import voiceProxySettings

logging_comp_name = 'checkConversationSignal'

#------- Check Conversation Signals  Methods -----------------


def wcsSignals(message):
	message = preCheckConversationSignal(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'preCheckConversationSignal -> Returning to Gateway', message)
		return message
	
	message = checkConversationSignal(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'checkConversationSignal -> Returning to Gateway', message)
		return message
	
	message = postCheckConversationSignal(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'postCheckConversationSignal -> Returning to Gateway', message)
		return message
	
	return message




def preCheckConversationSignal(message):
	
	return message

def checkConversationSignal(message):
	
	if check_wcsActionSignal(message,'askoriginal'):
		logging.info("Calling Conversation again based on signal")
		message['input']['text'] = message['context']['origInput']
		del message['output']
		del message['intents']
		message = callConversationService(message)
		message = wcsSignals(message)
		return message
		
	
		
	if check_DTMFSignal(message):
		logging.info("DTMF set from Convesation Service")
		return message

	
	if check_wcsHangUp(message):
		logging.info("Hangup")
		message = setEarlyReturn(message,'Conversation Signals Hangup -> Returning to Gateway')
		return message
		
	return message
	
	
def postCheckConversationSignal(message):
	return message


#------ EndCheck Conversation Signals Methods ---------------






#--------------- Signals from the Watson Conversation Dialog --------------	
def check_DTMFSignal(message):
	if 'context' in message:
		if 'cisContext' in message['context']:
			if 'cisDTMF' in message['context']['cisContext']:
				if 'enabled' in message['context']['cisContext']['cisDTMF']:
					return message['context']['cisContext']['cisDTMF']['enabled']
				else:
					return False


def check_wcsHangUp(message):
	if 'output' in message:
		if 'action' in message['output']:
			if message['output']['action'] == 'hangup':
				return True
			else:
				return False
				

#------------- End Signals from Help Gateway -----------------