#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
import voiceProxySettings


MUSIC_HOLD_ENABLED = False
MUSIC_HOLD = "http://10.2.2.216:5000/static/hold_music_01.wav"




def earlyReturn(message):
	if 'cisContext' in message['context']:
		if 'earlyReturn' in message['context']['cisContext']:
			return message['context']['cisContext']['earlyReturn']
	
	return False;
	
def setEarlyReturn(message, logmessage):
	message['context']['cisContext']['earlyReturn'] = True
	message['context']['cisContext']['earlyReturnMsg'] = logmessage
	
	return message


def getCisAttribute(attrib, message):
	if attrib in message['context']['cisContext']:
		return message['context']['cisContext'][attrib]
	else:
		return None
		
def clearCisAttribute(attrib, message):
	del message['context']['cisContext'][attrib]
	return message

def removeEntities(message):
	if 'entities' in message:
		del message['entities']
	return message

def removeIntents(message):
	if 'intents' in message:
		del message['intents']
	return message
#-------------- Polling Helper Methods -----------------------

def inPollingState(message):
	if 'cisPolling' in message['context']['cisContext']:
		if message['context']['cisContext']['cisPolling']:
			logging.debug("In Polling State")
			return True

	return False

def pollingTimeLeft(message):
	if 'cisPollTimeStamp' in message['context']['cisContext']:
		ts  = message['context']['cisContext']['cisPollTimeStamp']
		now = time.time()
		if (now-ts) < voiceProxySettings.POLLING_SLEEP_TIME:
			return (voiceProxySettings.POLLING_SLEEP_TIME) - (now-ts)
		else:
			return 0
	return 0
	
def startPolling(message):
	message['context']['vgwForceNoInputTurn'] = 'Yes'
	message['context']['cisContext']['cisPollTimeStamp'] = time.time()
	message['context']['cisContext']['cisPolling'] = True
		
	if MUSIC_HOLD_ENABLED:
		message['context']['vgwMusicOnHoldURL'] = MUSIC_HOLD
	return message


	
def stopPolling(message):
	if 'context' in message:
		if 'vgwForceNoInputTurn' in message['context']:
			del message['context']['vgwForceNoInputTurn']
		if 'vgwPostResponseTimeout' in message['context']:
			del message['vgwPostResponseTimeout']
		if 'cisPollTimeStamp' in message['context']['cisContext']:
			message['context']['cisContext']['cisPollTimeStamp'] = 0.0
		if 'cisPolling' in message['context']['cisContext']:
			message['context']['cisContext']['cisPolling'] = False
			
	return message
	
#-------------- End Polling Helper Methods -------------------

#--------------- Start of Checking for Conversation Signals --------------
# The two types of signals are:
# 1. Tell proxy and then the gateway we want to be in DTMF state
# 2. Tell proxy to take an action like do an API call and look something up

def checkConversationDTMFSignal(message):
	print("Nothing going on here")
	
def check_wcsActionSignal(message, signal):
	if 'output' in message:
		if 'action' in message['output']:
			if signal in message['output']['action']:
				return True
	
	return False

#--------------- End of Checking for Conversation Signals ----------------	