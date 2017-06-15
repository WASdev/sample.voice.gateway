import os, requests, json, string, datetime, logging, time

# ------------------------------------------------
# GLOBAL VARIABLES -------------------------------
# ------------------------------------------------


def init():

	global DTMF_ENABLED
	DTMF_ENABLED = False
	if 'DTMF_ENABLED' in os.environ:
		DTMF_ENABLED = os.environ['DTMF_ENABLED']

	global DTMF_LOCAL_DICT_ENABLED
	DTMF_LOCAL_DICT_ENABLED = True
	if 'DTMF_LOCAL_DICT_ENABLED' in os.environ:
		DTMF_LOCAL_DICT_ENABLED = os.environ['DTMF_LOCAL_DICT_ENABLED']
		
	global BARGE_IN_ENABLED
	BARGE_IN_ENABLED = False
	if 'BARGE_IN_ENABLED' in os.environ:
		BARGE_IN_ENABLED = os.environ['BARGE_IN_ENABLED']

	global APP_NAME_LOGGING
	APP_NAME_LOGGING='Siemens Cognitive Integration Server'
	if 'APP_NAME_LOGGING' in os.environ:
		APP_NAME_LOGGING = os.environ['APP_NAME_LOGGING']

	global POLLING_SLEEP_TIME
	POLLING_SLEEP_TIME=10
	if 'POLLING_SLEEP_TIME' in os.environ:
		POLLING_SLEEP_TIME = os.environ['POLLING_SLEEP_TIME']
	
	
	global CONVERSATION_TRACKING
	CONVERSATION_TRACKING= False
	if 'CONVERSATION_TRACKING' in os.environ:
		CONVERSATION_TRACKING = os.environ['CONVERSATION_TRACKING']

	global WEB_LOGGING
	WEB_LOGGING= False
	if 'WEB_LOGGING' in os.environ:
		WEB_LOGGING = os.environ['WEB_LOGGING']

	global POLLING_URL
	POLLING_URL = ''
	if 'POLLING_URL' in os.environ:
		POLLING_URL = os.environ['POLLING_URL']

	global POLLING_USERNAME
	POLLING_USERNAME = ''
	if 'POLLING_USERNAME' in os.environ:
		POLLING_USERNAME = os.environ['POLLING_USERNAME']

	global POLLING_PASSWORD
	POLLING_PASSWORD = ''
	if 'POLLING_PASSWORD' in os.environ:
		POLLING_PASSWORD = os.environ['POLLING_PASSWORD']

# Default should be True. False for deprecated WCS behavior.
	global REMOVE_ENTITIES
	REMOVE_ENTITIES = True
	if 'REMOVE_ENTITIES' in os.environ:
		REMOVE_ENTITIES = os.environ['REMOVE_ENTITIES']
	
# Default should be True. False for deprecated WCS behavior. 
	global REMOVE_INTENTS
	REMOVE_INTENTS = True
	if 'REMOVE_INTENTS' in os.environ:
		REMOVE_INTENTS = os.environ['REMOVE_INTENTS']
	
	global ALLOW_CUSTOMER_SET_WAIT 
	ALLOW_CUSTOMER_SET_WAIT= False
	if 'ALLOW_CUSTOMER_SET_WAIT' in os.environ:
		ALLOW_CUSTOMER_SET_WAIT = os.environ['ALLOW_CUSTOMER_SET_WAIT']
	
	global CHECK_INPUT_NUMBERS
	CHECK_INPUT_NUMBERS = False
	if 'CHECK_INPUT_NUMBERS' in os.environ:
		CHECK_INPUT_NUMBERS = os.environ['CHECK_INPUT_NUMBERS']
		

def generateState():
	state = {}
	state['cisContext'] = {}
	
	state['cisContext']['cisBargein']= BARGE_IN_ENABLED
	state['cisContext']['cisWebLogging']= WEB_LOGGING
	state['cisContext']['cisCustomerWait']= ALLOW_CUSTOMER_SET_WAIT
	
	state['cisContext']['cisDTMF']= {}
	state['cisContext']['cisDTMF']['enabled'] = DTMF_ENABLED
	state['cisContext']['cisDTMF']['localDictonary'] = DTMF_LOCAL_DICT_ENABLED
	
	state['cisContext']['cisPolling']= {}
	state['cisContext']['cisPolling']['sleepTime']= POLLING_SLEEP_TIME
	state['cisContext']['cisPolling']['URL']= POLLING_URL
	state['cisContext']['cisPolling']['username']= POLLING_USERNAME
	state['cisContext']['cisPolling']['password']= POLLING_PASSWORD
	
	return state

# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_PROFILE_API = os.path.join(APP_ROOT, 'callerProfileAPI')

	
