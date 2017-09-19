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
	
	if check_vgwPostResponseTimeout(message):
		logging.debug("RespTimeout")
		
	return message
	
	
def postCheckGatewaySignal(message):
	return message


#--------------- Signals from the SIP Gateway --------------	
def check_vgwPostResponseTimeout(message):
	return check_vgwSignal(message,'vgwPostResponseTimeout')
	
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
#------------- End Signals from Help Gateway -----------------


