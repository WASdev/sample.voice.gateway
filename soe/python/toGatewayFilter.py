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
from voicefilters import response_filter
from checkGatewaySignal import check_vgwHangUp
from checkDTMF import DTMFwaitState
from voiceProxyUtilities import setEarlyReturn, earlyReturn

logging_comp_name = "toGatewayFilter"
#------- To Gateway Filter Methods -----------------



def outputFilter(message):
	message = preToGatewayFilter(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'preToGatewayFilter -> Returning to Gateway', message)
		return message

	message = toGatewayFilter(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'toGatewayFilter -> Returning to Gateway', message)
		return message

	message = postToGatewayFilter(message)
	if earlyReturn(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'postToGatewayFilter -> Returning to Gateway', message)
		return message

	return message

def preToGatewayFilter(message):
	
	return message

def toGatewayFilter(message):

	if check_vgwHangUp(message):
		return message

	if DTMFwaitState(message):
		if 'output' in message:
			if 'text' in message['output']:
				message = response_filter(message)
		return message
		
		
	# Time to hang up
	if endOfSession(message):
		if 'context' in message:
			message['context']['vgwHangUp'] = 'Yes'
	
	# This is a good time to check if words need to be replace
	# For example the RX should be Prescription. We only do this when the TTS engine can not be trained.
	# The voiceProxyWordTag plugin can be used.
	### Holding place for wordtag call	
				
	# Cleaning up the response
	if 'output' in message:
		if 'text' in message['output']:
			message = response_filter(message)
		else:
			logging.critical("\n\n\ntext node is not in the output JSON object. Something serious is wrong\n\n\n")

	else:
		logging.critical("\n\n\nOutput node is not in the JSON object. Something serious is wrong\n\n\n")

		
	
	# Temp Fix for Gateway	
	message = stuffEntitiesIntents(message)
	message = removeInput(message)

	return message

def postToGatewayFilter(message):
	return message



	
#------ End To Gateway Filter Methods ---------------------




# -------------- Bug in Gateway Fixer Method ----------------
def removeInput(message):
	if 'input' in message:
		logging.debug("Removing input node of JSON")
		del message['input']
		logging.debug(message)
		
	return message

#Short term fix for Gateway issue with Entities and Intents not being preserved

def stuffEntitiesIntents(message):
	if 'entities' in message:
		if 'context' in message:
			message['context']['soeEntities'] = message['entities']
			#causes NPE in Voice gateway - see issue 35
			#del message['entities']
	if 'intents' in message:
		if 'context' in message:
			message['context']['soeIntents'] = message['intents']	
			#causes NPE in Voice gateway - see issue 35
			#del message['intents']	
	return message

# -------------- End Bug in Gateway Fixer Method ----------------	

#----------------- Internal Utility Methods -----------------

def endOfSession(message):
	if 'context' in message:
		if 'endSession' in message['context']:
			return message['context']['endSession']
	return False
	

def filter_response_line_level(message):
	return message
	
def filter_response_message_level(message):
	return message

#----------------- End Internal Utility Method --------------
