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
from voiceProxyUtilities import remove_wcsActionSignal

logging_comp_name = "toGatewayFilter"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#------- To Gateway Filter Methods -----------------



def outputFilter(message):

	message = toGatewayFilter(message)

	return message

def toGatewayFilter(message):
	
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
	
	# Removing the action signal from the Conversation Service
	remove_wcsActionSignal(message)

	return message



	
#------ End To Gateway Filter Methods ---------------------


# -------------- End Bug in Gateway Fixer Method ----------------	

#----------------- Internal Utility Methods -----------------

def endOfSession(message):
	if 'context' in message:
		if 'endSession' in message['context']:
			return message['context']['endSession']
	return False

#----------------- End Internal Utility Method --------------