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
import voiceProxyUtilities

logging_comp_name = "fromGatewayFilter"
#------- From Gateway Filter Methods -----------------


def inputFilters(message):
	
	
	# Need to see if bargin is needed and if so set it
	message = setBargeIn(message)
	
	# Set the cisContext Object
	message = createCisContext(message)
	
	message = preFromGatewayFilter(message)
	
	message = fromGatewayFilter(message)
	
	message = postFromGatewayFilter(message)
	
	return message




def preFromGatewayFilter(message):
	# Temp Fix for Gateway
	message = grabEntitiesIntents(message)
	
	# Conversation doesn't want intents for some reason
	if voiceProxySettings.REMOVE_INTENTS:
		message = voiceProxyUtilities.removeIntents(message)

	if voiceProxySettings.REMOVE_ENTITIES:
		message = voiceProxyUtilities.removeEntities(message)
				
	return message

def fromGatewayFilter(message):
	
	if 'context' in message:
		if 'vgwSessionID' in message['context']:
			logging.info("API Call -> SessionID: " + message['context']['vgwSessionID'])
		else:
			logging.info('API Call -> Serious Error, no vgwSessionID in Context')
	
	
	if voiceProxySettings.CHECK_INPUT_NUMBERS:
		message = check_numbers(message)
	
	
	addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'FromGatewayFilter Method', message)
	
	logging.debug(message)
	
	
	# Signal for Conversation Service that messages are coming from Voice Gateway
	if 'context' in message:
		message['context']['voiceFlow'] = True

	return message

def postFromGatewayFilter(message):
	return message

#------ End From Gateway Filter Methods ---------------------

def check_numbers(message):
	#look at the input and convert the number words to digits
	num_digit ={}
	num_digit["one"] = "1"
	num_digit["two"] = "2"
	num_digit["to"] = "2"
	num_digit["too"] = "2"
	
	num_digit["three"] = "3"
	num_digit["four"] = "4"
	num_digit["for"] = "4"
	
	num_digit["zero"] = "0"
	num_digit["five"] = "5"
	num_digit["six"] = "6"
	num_digit["seven"] = "7"
	num_digit["eight"] = "8"
	num_digit["nine"] = "9"
	
	logging.debug("Looking to check for numbers\n\n")
	
	
	phrase = message['input']['text']
	logging.debug("Spoken Message: " + phrase)
	nphrase = swap_phrase(num_digit,phrase)
	nphrase = nphrase.rstrip()
	logging.debug("Cleansed Message: " + nphrase)
	message['input']['text'] = nphrase
	return message


def swap_phrase(ssml_dict,phrase):
	nphrase = phrase
	for ssml_key in ssml_dict:
		nphrase = nphrase.replace(ssml_key,ssml_dict[ssml_key])
	
	logging.debug("Swap returning " + nphrase)
	return nphrase


def setBargeIn(message):
	if 'context' in message:
		if voiceProxySettings.BARGE_IN_ENABLED:
			message['context']['vgwAllowBargeIn'] = 'Yes'
		else:		
			message['context']['vgwAllowBargeIn'] = 'No'
		
	return message

def createCisContext(message):
	if 'context' in message:
		if 'cisContext' in message['context']:
			return message
		else:
			message['context']['cisContext'] = {}
			return message
	else:
		logging.warn("No Context Object in JSON")
		return message

def grabEntitiesIntents(message):
	if 'context' in message:
		if 'soeEntities' in message['context']:
			message['entities'] = message['context']['soeEntities']
			message['context']['soeEntities'] = ''
		if 'soeIntents' in message['context']:
			message['intents'] = message['context']['soeIntents']
			message['context']['soeIntents'] = ''
	return message
	