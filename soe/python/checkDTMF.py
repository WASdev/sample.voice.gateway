# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
from weblogger import addLogEntry
from callerProfileAPI.callerProfileAPI import getCardByName
import voiceProxySettings


logging_comp_name = "checkDTMF"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


	
#------- Check DTMF Methods -----------------

def dtmf(message):
		
	message = checkDTMF(message)

	return message

def checkDTMF(message):
				
	return message