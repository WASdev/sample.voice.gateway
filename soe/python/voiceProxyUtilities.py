#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
import voiceProxySettings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MUSIC_HOLD_ENABLED = False
MUSIC_HOLD = "http://10.2.2.216:5000/static/hold_music_01.wav"


def getCisAttribute(attrib, message):
	if attrib in message['context']['cisContext']:
		return message['context']['cisContext'][attrib]
	else:
		return None
		
def clearCisAttribute(attrib, message):
	del message['context']['cisContext'][attrib]
	return message
	
#-------------- End Polling Helper Methods -------------------


def replaceOutputTagValue(message, tag, value):
	logging.info("Tag is: "  + tag + " value is " + str(value))
	logging.info("Output is: ")
	logging.info(message['output'])
	if 'output' in message and 'text' in message['output'] and len(message['output']['text'])>0:
		for idx, line in enumerate(message['output']['text']):
			if tag in line:
				message['output']['text'][idx] = line.replace(tag,str(value))
	
	
	return message
	
def check_wcsActionSignal(message, signal):
	if 'output' in message:
		if 'action' in message['output']:
			if signal in message['output']['action']:
				return True
	
	return False

def remove_wcsActionSignal(message):
	if 'output' in message:
		if 'action' in message['output']:
			del message['output']['action']
#--------------- End of Checking for Conversation Signals ----------------	