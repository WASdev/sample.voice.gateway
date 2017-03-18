# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
from weblogger import addLogEntry
from dtmfService import decode

import voiceProxySettings
from voiceProxyUtilities import setEarlyReturn, earlyReturn


logging_comp_name = "checkDTMF"


	
#------- Check DTMF Methods -----------------

def dtmf(message):
	if voiceProxySettings.DTMF_ENABLED:
		message = preCheckDTMF(message)
		if earlyReturn(message):
			addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'preCheckDTMF -> Returning to Gateway', message)
			return message
		
		message = checkDTMF(message)
		if earlyReturn(message):
			addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'checkDTMF -> Returning to Gateway', message)
			return message
	
		message = postCheckDTMF(message)
		if earlyReturn(message):
			addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'postcheckDTMF -> Returning to Gateway', message)
			return message


	return message


def preCheckDTMF(message):
	return message

def checkDTMF(message):
	
	if DTMFwaitState(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'Entering checkDTMF', message)
		dtmf = dtmfCheck(message)
		message['context']['cisContext']['cisDTMF'] = dtmf
		if dtmf['Error']:
			logging.debug("DTMF Error: " + dtmf['Error_Message'])	
		else:
			# ------ special logic for client -------
			if 'connexusID' in message['context'] and len(message['context']['connexusID']) == 0:
				if dtmf['captureComplete']: 
					logging.debug('Changing text to ConnexusID: ' +  dtmf['Words'][0])
					message['input']['text'] = dtmf['Words'][0]
			
	return message

def postCheckDTMF(message):
	
	if DTMFwaitState(message):
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'Entering PostCheckDTMF', message)
		if 'input' in message:
			if 'text' in message['input']:
				if len(message['input']['text'])== 0:
					return message
				
		if 'context' in message:
			if 'cisDTMF' in message['context']['cisContext']:
				if 'Error' in message['context']['cisContext']['cisDTMF']:
					if message['context']['cisContext']['cisDTMF']['Error'] == False:
						if message['context']['cisContext']['cisDTMF']['captureComplete'] == False:
							digits = message['context']['cisContext']['cisDTMF']
							#addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'DTMF Capture', message)
							message = setEarlyReturn(message,'DTMF Capture -> Return to Gateway')
							return message
					else:
						if message['context']['cisContext']['cisDTMF']['Error_Code'] == 3:
							message = handleDTMFErrorCodeThree(message)
							addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'DTMF  ErrorCode 3', message)
							message = setEarlyReturn(message,'DTMF  ErrorCode 3 -> Return to Gateway')
							return message
	return message

#------ End Check DTMF Methods ---------------


def dtmfCheck(message):
	
	dtmf = createDefaultDTMFObject()
	# Looking for # to signal done collecting digits
	if message['input']['text'] == '#':
		digits = dtmfList(message)
		dtmf['Words'] = decode(digits)
		if len(dtmf['Words']) == 1:
			dtmf['digits'] = ''
			dtmf['captureComplete'] = True
		if len(dtmf['Words']) > 1:
			dtmf['Error'] = True
			dtmf['Error_Code'] = 1
			dtmf['Error_Message'] = 'More than one result'

		if len(dtmf['Words']) == 0:
			dtmf['Error'] = True
			dtmf['Error_Code'] = 2
			dtmf['Error_Message'] = 'No results'
	else:
		# Since we are in DTMF mode, we need to get rid of any words spoken
		if message['input']['text'].isdigit():
			check_numbers(message)
			digits = dtmfList(message) + message['input']['text']
			dtmf['digits'] = digits
			return dtmf
			
		if len(message['input']['text'])== 0:
			return dtmf
			
		else:
			logging.debug("Message has a word instead of a digit")
			dtmf['Error_Code'] = 3
			dtmf['Error_Message'] = 'Spoken Text when expecting DTMF digit'
			dtmf['Error'] = True
			
			if 'cisDTMF' in message['context']['cisContext']:
				if 'digits' in message['context']['cisContext']['cisDTMF']:
					dtmf['digits'] = message['context']['cisContext']['cisDTMF']['digits']
			
			
	return dtmf

def handleDTMFErrorCodeThree(message):
	stdmsg = ["Sorry, we are only expecting Keypad entries at this time."]
	stdmsg = createExistingDTMFDigitsMsg(message, stdmsg)
	
		
	outp = {}
	outp['text'] = stdmsg
	message['output'] = outp
	return message					


def createDefaultDTMFObject():
	dtmf = {}
	dtmf['enabled'] = False 
	dtmf['captureComplete'] = False 
	dtmf['digits'] = ''
	dtmf['Error'] = False
	dtmf['Error_Code'] = 0
	dtmf['Error_Message'] =''
	dtmf['Words'] = []
	dtmf['Action'] = ''
	return dtmf

def dtmfList(message):
	if 'context' in message:
		if 'cisDTMF' in message['context']['cisContext']:
			if 'digits' in message['context']['cisContext']['cisDTMF']:
				return message['context']['cisContext']['cisDTMF']['digits']
	return ""		
	
def handleDTMFTimeout(message):
	stdmsg = ["Please make sure you hit the hash key to complete your keypad entry."]
	createExistingDTMFDigitsMsg(message, stdmsg)

	outp = {}
	outp['text'] = stdmsg
	message['output'] = outp
	return message		

def createExistingDTMFDigitsMsg(message, stdmsg):
	if 'cisDTMF' in message['context']['cisContext']:
		if 'digits' in message['context']['cisContext']['cisDTMF']:
			if len(message['context']['cisContext']['cisDTMF']['digits'])>0:
				digs = message['context']['cisContext']['cisDTMF']['digits']
				stdmsg.append("You have already typed " + digs)
				stdmsg = ssml_filter(stdmsg)
			return stdmsg
	
def DTMFwaitState(message):
	if voiceProxySettings.DTMF_ENABLED:
		if 'context' in message:
			if 'cisDTMF' in message['context']['cisContext']:
				if message['context']['cisContext']['cisDTMF']['captureComplete'] == False:
					return True
				else:
					return False
			else:
				return True
		else:
			return False
	else:
		return False					
	
	return False


def handleDTMFTimeout(message):
	stdmsg = ["Please make sure you hit the hash key to complete your keypad entry."]
	createExistingDTMFDigitsMsg(message, stdmsg)

	outp = {}
	outp['text'] = stdmsg
	message['output'] = outp
	return message		


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
#	nphrase = nphrase.replace(" ","")
#	nphrase = nphrase.lower()
	nphrase = nphrase.rstrip()
	logging.debug("Cleansed Message: " + nphrase)
	message['input']['text'] = nphrase


		
def swap_phrase(ssml_dict,phrase):
	nphrase = phrase
	for ssml_key in ssml_dict:
		nphrase = nphrase.replace(ssml_key,ssml_dict[ssml_key])
	
	logging.debug("Swap returning " + nphrase)
	return nphrase

#--------- Utility Methods ------------

def setEarlyReturn(message, logmessage):
	message['context']['cisContext']['earlyReturn'] = True
	message['context']['cisContext']['earlyReturnMsg'] = logmessage
	
	return message


def ssml_filter(message):
	ssml_dict = set_ssml_dict()
	outp = message
	logging.debug("SSML Filtering")
	for i, phrase in enumerate(outp):
		outp[i] = swap_phrase(ssml_dict,outp[i])
		outp[i] = check_str_num(outp[i])
	

	outp.insert(0,"<speak version=\"1.0\">")
	outp.insert(1,'<voice-transformation type="Custom" timbre="Breeze" breathiness="80%"  rate="10%" timbre_extent="20%" >')
	outp.append('</voice-transformation>')
	outp.append("</speak>")
	#logging.debug(outp)
	
	return outp

def set_ssml_dict():
	ssml_dict={}
	ssml_dict['.'] = " <break strength=\"strong\"></break>"
	ssml_dict[','] = " <break strength=\"medium\"></break>"
	ssml_dict["alphanumeric"] = "alpha numeric"
	return ssml_dict




