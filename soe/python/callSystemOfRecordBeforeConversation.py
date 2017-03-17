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

logging_comp_name = "callSystemOfRecordBeforeConversation"



#------- Check SOR Before Conversation Methods -----------------
def callSORBeforeConv(message):
	message = preCallSystemOfRecordBeforeConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'preCallSystemOfRecordBeforeConversation -> Returning to Gateway', message)
		return message
	
	message = callSystemOfRecordBeforeConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'callSystemOfRecordBeforeConversation -> Returning to Gateway', message)
		return message

	message = postCallSystemOfRecordBeforeConversation(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'postCallSystemOfRecordBeforeConversation -> Returning to Gateway', message)
		return message
	
	return message


def preCallSystemOfRecordBeforeConversation(message):
	return message

def callSystemOfRecordBeforeConversation(message):
	return message

def postCallSystemOfRecordBeforeConversation(message):
	return message

#------ End Check SOR Before Conversation Methods ---------------