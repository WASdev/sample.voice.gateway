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


logging_comp_name = "checkUtterance"


def utterance(message):
	message = preCheckUtterance(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'preCheckUtterance -> Returning to Gateway', message)
		return message
	
	message = checkUtterance(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'checkUtterance -> Returning to Gateway', message)
		return message
	
	message = postCheckUtterance(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'postCheckUtterance -> Returning to Gateway', message)
		return message

	return message

def preCheckUtterance(message):
	return message

def checkUtterance(message):
	return message

def postCheckUtterance(message):
	return message

