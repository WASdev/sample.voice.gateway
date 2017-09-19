# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
from weblogger import addLogEntry

from voiceProxyUtilities import check_wcsActionSignal
from callConversation import callConversationService

import voiceProxySettings

logging_comp_name = 'checkConversationSignal'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#------- Check Conversation Signals  Methods -----------------


def wcsSignals(message):
	
	message = checkConversationSignal(message)
	
	return message

def checkConversationSignal(message):
	
	if check_wcsActionSignal(message,'askoriginal'):
		logging.info("Calling Conversation again based on signal")
		message['input']['text'] = message['context']['origInput']
		del message['output']
		del message['intents']
		del message['entities']
		message = callConversationService(message)
		message = wcsSignals(message)
		return message
		
	return message