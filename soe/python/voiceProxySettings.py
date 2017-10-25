import os, requests, json, string, datetime, logging, time

# ------------------------------------------------
# GLOBAL VARIABLES -------------------------------
# ------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init():

	global APP_NAME_LOGGING
	APP_NAME_LOGGING='Demo Voice Proxy Server SOE'
	if 'APP_NAME_LOGGING' in os.environ:
		APP_NAME_LOGGING = os.environ['APP_NAME_LOGGING']
	
	
	global CONVERSATION_TRACKING
	CONVERSATION_TRACKING= False
	if 'CONVERSATION_TRACKING' in os.environ:
		CONVERSATION_TRACKING = os.environ['CONVERSATION_TRACKING']

	global WEB_LOGGING
	WEB_LOGGING= False
	if 'WEB_LOGGING' in os.environ:
		WEB_LOGGING = os.environ['WEB_LOGGING']


	checkConversationEnv()
	
def checkConversationEnv():
	if 'CONVERSATION_WORKSPACE_ID' not in os.environ:
		logging.info("ERROR no CONVERSATION_WORKSPACE_ID Defined!")
	if 'CONVERSATION_USERNAME' not in os.environ:
		logging.info("Error no CONVERSATION_USERNAME Defined!")
	if 'CONVERSATION_PASSWORD' not in os.environ:
		logging.info("Error no CONVERSATION_PASSWORD Defined!")
	if 'CONVERSATION_VERSION' not in os.environ:
		logging.info("Error no CONVERSATION_VERSION Defined!")		

# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_PROFILE_API = os.path.join(APP_ROOT, 'callerProfileAPI')

	