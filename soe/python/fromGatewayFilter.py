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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#------- From Gateway Filter Methods -----------------


def inputFilters(message):
	
	# Set the cisContext Object
	message = createCisContext(message)
	
	message = fromGatewayFilter(message)
	
	return message


def fromGatewayFilter(message):
	
	if 'context' in message:
		if 'vgwSessionID' in message['context']:
			logging.info("API Call -> SessionID: " + message['context']['vgwSessionID'])
		else:
			logging.info('API Call -> Serious Error, no vgwSessionID in Context')
	
	
	addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'FromGatewayFilter Method', message)
	
	logging.debug(message)
	

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
	