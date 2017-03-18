# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
from weblogger import addLogEntry
from checkDTMF import handleDTMFTimeout, DTMFwaitState
from voiceProxyUtilities import setEarlyReturn, inPollingState, startPolling, pollingTimeLeft, earlyReturn

import voiceProxySettings

logging_comp_name = 'checkGatewaySignal'

#------- Check Input From Gateway Methods -----------------


def signals(message):
	message = preCheckGatewaySignal(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'preCheckGatewaySignal -> Returning to Gateway', message)
		return message
	
	message = checkGatewaySignal(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'checkGatewaySignal -> Returning to Gateway', message)
		return message
	
	message = postCheckGatewaySignal(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'postCheckGatewaySignal -> Returning to Gateway', message)
		return message
	
	return message




def preCheckGatewaySignal(message):
	
	return message

def checkGatewaySignal(message):
	
	if check_vgwPostResponseTimeout(message):
		logging.debug("RespTimeout")
		if inPollingState(message):
			logging.info("in Polling State with RespTimeout Message")
			#message = startPolling(message)
			message = setEarlyReturn(message,'In Polling State and Gateway Signals ResTimeout -> Returning to Gateway')
			return message
		
		if DTMFwaitState(message):
			logging.info("Timeout while in DTMF WaitState")
			message = handleDTMFTimeout(message)
			message = setEarlyReturn(message,'Gateway Signals RespTimeout in DTMF Waitstate -> Returning to Gateway')
			return message

		
		message = setEarlyReturn(message,'Returning from RespTimeout')
		return message

	if check_vgwNoInputTurn(message) and inPollingState(message):
		logging.info("NoInputTurn")
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'Gateway Signals NoInputTurn and in Polling WaitState', message)
		time.sleep(pollingTimeLeft(message))
		return message
	
	if check_vgwHangUp(message):
		logging.info("Hangup")
		message = setEarlyReturn(message,'Gateway Signals Hangup -> Returning to Gateway')
		return message
		
	return message
	
	
def postCheckGatewaySignal(message):
	return message


#------ EndCheck Input From Gateway Methods ---------------






#--------------- Signals from the SIP Gateway --------------	
def check_vgwPostResponseTimeout(message):
	return check_vgwSignal(message,'vgwPostResponseTimeout')

def check_vgwNoInputTurn(message):
	return check_vgwSignalInString(message,'vgwNoInputTurn')

def check_vgwHangUp(message):
	return check_vgwSignal(message,'vgwHangUp')
	
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


