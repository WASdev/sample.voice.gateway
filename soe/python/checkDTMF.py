# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
from weblogger import addLogEntry
from callerProfileAPI.callerProfileAPI import getCardByName, getCustomerByName, setCreditCard, updateCustomer
import voiceProxySettings


logging_comp_name = "checkDTMF"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


	
#------- Check DTMF Methods -----------------

def dtmf(message):
		
	message = checkDTMF(message)

	return message

def checkDTMF(message):
	if 'context' in message:
		if 'collectedDTMF' in message['context']:
			del message['context']['collectedDTMF']

			if 'input' in message:
				cardNumber = message['input']['text']
				message['input']['text'] = 'dtmfSuccess'
			else:
				return message

			#Add the credit card number to the user
			name = message['context']['callerProfile']['firstname']
			cardType = message['context']['profile']['cardname']
			customer = getCustomerByName(name.strip())
			setCreditCard(customer, cardType, cardNumber)
			updateCustomer(customer)
			
	return message