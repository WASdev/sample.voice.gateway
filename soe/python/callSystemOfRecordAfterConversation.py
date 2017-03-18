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
from voiceProxyUtilities import setEarlyReturn, earlyReturn, check_wcsActionSignal
from callerProfileAPI.callerProfileAPI import getProfileByName, makePayment, updateProfile
from callConversation import callConversationService
from checkConversationSignal import  wcsSignals

logging_comp_name = "callSystemOfRecordAfterConversation"



#------- Check SOR After Conversation Methods -----------------
def callSORAfterConv(message):

	message = preCallSystemOfRecordAfterConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'preCallSystemOfRecordAfterConversation -> Returning to Gateway', message)
		return message

	message = callSystemOfRecordAfterConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'callSystemOfRecordAfterConversation -> Returning to Gateway', message)
		return message
		
	message = postCallSystemOfRecordAfterConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'postCallSystemOfRecordAfterConversation -> Returning to Gateway', message)
		return message
		
	return message	

def preCallSystemOfRecordAfterConversation(message):
	return message

def callSystemOfRecordAfterConversation(message):
	if check_wcsActionSignal(message,'getProfile'):
		logging.info("Grabing the user profile")
		message = doGetProfile(message)
	
	if check_wcsActionSignal(message,'makePayment'):
		logging.info("Calling API to make a payment")
		if doMakePayment(message):
			message = doGetProfile(message)
			if 'payment' in message['context']:
				del message['context']['payment']
	
	if check_wcsActionSignal(message,'checkBalanceAskAgain'):
		logging.info("Checking balance and Calling Conversation again based on signal")
		message['input']['text'] = message['context']['origInput']
		del message['output']
		del message['intents']
		
		
		message = doGetProfile(message)
		message = callConversationService(message)
		message = wcsSignals(message)
		message = callSORAfterConv(message)
		
		return message
			
			
		
	return message

def postCallSystemOfRecordAfterConversation(message):
	return message

#------ End Check SOR After Conversation Methods ---------------

def doMakePayment(message):
	name = message['context']['callerProfile']['firstname']
	profile = getProfileByName(name)
	loan = message['context']['payment']['type']
	account =message['context']['payment']['account']
	amount = message['context']['payment']['amount']
	 
	if makePayment(profile,loan,account,amount):
		updateProfile(profile)
		return True
		
	else:
		return False

def doGetProfile(message):
	name = message['context']['callerProfile']['firstname']
	profile = getProfileByName(name)
	message['context']['profile'] = profile
	return message


