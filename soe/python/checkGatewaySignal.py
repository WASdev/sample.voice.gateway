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

logging_comp_name = 'checkGatewaySignal'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#------- Check Input From Gateway Methods -----------------


def signals(message):
	
	message = checkGatewaySignal(message)
	
	return message


def checkGatewaySignal(message):
	

	return message


#--------------- Signals from the SIP Gateway --------------	
def check_vgwPostResponseTimeout(message):
	return check_vgwSignal(message,'vgwPostResponseTimeout')

def checkCardName(message):
	if 'context' in message:
		if 'profile' in message['context']:
			if 'cardname' in message['context']['profile']:
				logging.info(message['input']['text'])
				message['context']['profile']['cardname'] = message['input']['text']
	
def check_vgwSignal(message, signal):
	if 'input' in message:
		if 'text' in message['input']:
			if message['input']['text'] == signal:
				return True
	
	return False

def check_vgwSignalInString(message, signal):
	if 'input' in message:
		if 'text' in message['input']:
			if signal in message['input']['text']:
				return True
	
	return False