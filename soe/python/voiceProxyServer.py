# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time

from os.path import join, dirname
from flask import Flask, request, render_template, redirect, url_for, Response
from voicefilters import response_filter, check_utterance, need_connexusID, check_ssml_number, cleanResponseForGateway
from weblogger import addLogEntry
from fromGatewayFilter import inputFilters
from checkGatewaySignal import signals
from checkClientWaitState import waitState
from checkDTMF import dtmf
from checkUtterance import utterance
from callSystemOfRecordBeforeConversation import callSORBeforeConv
from callConversation import callConversationService
from checkPollingBackend import pollBackend
from callSystemOfRecordAfterConversation import callSORAfterConv
from checkConversationSignal import wcsSignals
from toGatewayFilter import outputFilter
import voiceProxyUtilities
import voiceProxySettings

voiceProxySettings.init()


# ------------------------------------------------
# FLASK ------------------------------------------
# ------------------------------------------------
app = Flask(__name__)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging_comp_name = "Voice Proxy Main Loop"

@app.route('/docs/CognitiveIntegrationServiceServer')
def documentPage():
      return app.send_static_file('docs/CognitiveIntegrationServiceServer.html')


@app.route('/docs/images/image00.png')
def documentImage():
      return app.send_static_file('docs/images/image00.png')
      	
# ------------- Main loop for CIS ----------------

@app.route('/v1/workspaces/<spaceid>/<msg>', methods=['POST'])
def restVoiceGatewayEntry(spaceid,msg):	
	resp_data = voiceGatewayEntry(spaceid,msg)
	return Response(resp_data, mimetype='application/json',status=200)
	
def voiceGatewayEntry(spaceid,msg):
	#Get data from post -- should be in the form of a conversation message	
	message = json.loads(request.data)

	##### First Check to see if the message passed to the Server is valid format #######
	if not checkGatewayMessage(message):
		# Need to know how to signal the Gateway something is wrong
		message = returningEarlyCleanup(message,'Gateway Message Check Failed -> Returning to Gateway')
		return json.dumps(message, separators=(',',':'))

	addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'New API Call', message)
	message = inputFilters(message)
	if earlyReturn(message):
		message = returningEarlyCleanup(message,'inputFilters -> Returning to Gateway')
		return json.dumps(message, separators=(',',':'))

	message = signals(message)
	if earlyReturn(message):
		message = returningEarlyCleanup(message,'signals -> Returning to Gateway')
		return json.dumps(message, separators=(',',':'))
	
	message = waitState(message)
	if earlyReturn(message):
		message = returningEarlyCleanup(message,'waitState -> Returning to Gateway')
		return json.dumps(message, separators=(',',':'))
	
	message = dtmf(message)
	if earlyReturn(message):
		message = returningEarlyCleanup(message,'dtmf -> Returning to Gateway')
		return json.dumps(message, separators=(',',':'))
	
	message = utterance(message)
	if earlyReturn(message):
		message = returningEarlyCleanup(message,'utterance -> Returning to Gateway')
		return json.dumps(message, separators=(',',':'))
		
	message = pollBackend(message)
	if earlyReturn(message):
		message = returningEarlyCleanup(message,'pollbackend -> Returning to Gateway')
		return json.dumps(message, separators=(',',':'))
		
	message = callSORBeforeConv(message)
	if earlyReturn(message):
		message = returningEarlyCleanup(message,'callBackend1 -> Returning to Gateway')
		return json.dumps(message, separators=(',',':'))
		
	message = callConversationService(message)
	if earlyReturn(message):
		message = returningEarlyCleanup(message,'callConversation -> Returning to Gateway')
		return json.dumps(message, separators=(',',':'))
	
	message = wcsSignals(message)
	if earlyReturn(message):
		message = returningEarlyCleanup(message,'callWcsSignal -> Returning to Gateway')
		return json.dumps(message, separators=(',',':'))
	
	
	message = callSORAfterConv(message)
	if earlyReturn(message):
		message = returningEarlyCleanup(message,'callBackend2 -> Returning to Gateway')
		return json.dumps(message, separators=(',',':'))
	
	message = outputFilter(message)
	if earlyReturn(message):
		message = returningEarlyCleanup(message,'outputFilters -> Returning to Gateway')
		return json.dumps(message, separators=(',',':'))
	
	
	# Finally Returning to Gateway
	addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'Normal Return to Gateway', message)
	return json.dumps(message, separators=(',',':'))
	



#-------------- Gateway Utility Methods ----------------------
# First method calldd 
def checkGatewayMessage(message):
	return True


def earlyReturn(message):
	return voiceProxyUtilities.earlyReturn(message)
	
def returningEarlyCleanup(message, logmessage):
	earlyMsg = voiceProxyUtilities.getCisAttribute('earlyReturnMsg',message)
	if earlyMsg and len(earlyMsg)>0:
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, earlyMsg, message)
		message = voiceProxyUtilities.clearCisAttribute('earlyReturn',message)
		message = voiceProxyUtilities.clearCisAttribute('earlyReturnMsg',message)
	else:
		addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, logmessage, message)
		message = voiceProxyUtilities.clearCisAttribute('earlyReturn',message)
		message = voiceProxyUtilities.clearCisAttribute('earlyReturnMsg',message)	
	
	message = outputFilter(message)
	
	return message

#-------------- End Gateway Utility Methods ------------------



#-------------- API Methods ----------------------------------
@app.route('/cis/bargein', methods=['POST','GET', 'PUT'])
def apiBargin():
	if request.data:
		data = json.loads(request.data)
		state = voiceProxySettings.generateState();
	
	
		if request.method == 'POST':
			if 'cisBargein' in data['cisContext']:
				voiceProxySettings.BARGE_IN_ENABLED = data['cisContext']['cisBargein']
		
		if request.method == 'PUT':
			if 'cisBargein' in data['cisContext']:
				voiceProxySettings.BARGE_IN_ENABLED = data['cisContext']['cisBargein']
			
	if request.method == 'GET':
		state = voiceProxySettings.generateState();
	
	state = voiceProxySettings.generateState();
	
	
	resp_data =  json.dumps(state, separators=(',',':'))
	return Response(resp_data, mimetype='application/json',status=200)

@app.route('/cis/weblogging', methods=['POST','GET', 'PUT'])
def apiWeblogging():
	if request.data:
		data = json.loads(request.data)
		state = voiceProxySettings.generateState();
	
	
		if request.method == 'POST':
			if 'cisWebLogging' in data['cisContext']:
				voiceProxySettings.WEB_LOGGING = data['cisContext']['cisWebLogging']
		
		if request.method == 'PUT':
			if 'cisWebLogging' in data['cisContext']:
				voiceProxySettings.WEB_LOGGING = data['cisContext']['cisWebLogging']
			
	if request.method == 'GET':
		state = voiceProxySettings.generateState();
	
	state = voiceProxySettings.generateState();
	
	
	resp_data =  json.dumps(state, separators=(',',':'))
	return Response(resp_data, mimetype='application/json',status=200)

@app.route('/cis/customerWait', methods=['POST','GET', 'PUT'])
def apiCustomerWait():
	if request.data:
		data = json.loads(request.data)
		state = voiceProxySettings.generateState();
	
	
		if request.method == 'POST':
			if 'cisCustomerWait' in data['cisContext']:
				voiceProxySettings.ALLOW_CUSTOMER_SET_WAIT = data['cisContext']['cisCustomerWait']
		
		if request.method == 'PUT':
			if 'cisCustomerWait' in data['cisContext']:
				voiceProxySettings.ALLOW_CUSTOMER_SET_WAIT = data['cisContext']['cisCustomerWait']
			
	if request.method == 'GET':
		state = voiceProxySettings.generateState();
	
	state = voiceProxySettings.generateState();
	
	
	resp_data =  json.dumps(state, separators=(',',':'))
	return Response(resp_data, mimetype='application/json',status=200)

@app.route('/cis/dtmf', methods=['POST','GET', 'PUT'])
def apidtmf():
	if request.data:
		data = json.loads(request.data)
		state = voiceProxySettings.generateState();
	
	
		if request.method == 'POST':
			if 'cisDTMF' in data['cisContext']:
				if 'enabled' in data['cisContext']['cisDTMF']:
					voiceProxySettings.DTMF_ENABLED = data['cisContext']['cisDTMF']['enabled']
			
		if request.method == 'PUT':
			if 'cisDTMF' in data['cisContext']:
				if 'enabled' in data['cisContext']['cisDTMF']:
					voiceProxySettings.DTMF_ENABLED = data['cisContext']['cisDTMF']['enabled']
			
	if request.method == 'GET':
		state = voiceProxySettings.generateState();
	
	state = voiceProxySettings.generateState();
	
	
	resp_data =  json.dumps(state, separators=(',',':'))
	return Response(resp_data, mimetype='application/json',status=200)


@app.route('/cis/polling', methods=['POST','GET', 'PUT'])
def apiPolling():
	if request.data:
		data = json.loads(request.data)
		state = voiceProxySettings.generateState();
	
	
		if request.method == 'POST':
			if 'cisPolling' in data['cisContext']:
				if 'sleepTime' in data['cisContext']['cisPolling']:
					voiceProxySettings.POLLING_SLEEP_TIME = data['cisContext']['cisPolling']['sleepTime']
				if 'URL' in data['cisContext']['cisPolling']:
					voiceProxySettings.POLLING_URL = data['cisContext']['cisPolling']['URL']
				if 'username' in data['cisContext']['cisPolling']:
					voiceProxySettings.POLLING_USERNAME = data['cisContext']['cisPolling']['username']
				if 'password' in data['cisContext']['cisPolling']:
					voiceProxySettings.POLLING_PASSWORD = data['cisContext']['cisPolling']['password']
		
		
		if request.method == 'PUT':
			if 'cisPolling' in data['cisContext']:
				if 'sleepTime' in data['cisContext']['cisPolling']:
					voiceProxySettings.POLLING_SLEEP_TIME = data['cisContext']['cisPolling']['sleepTime']
				if 'URL' in data['cisContext']['cisPolling']:
					voiceProxySettings.POLLING_URL = data['cisContext']['cisPolling']['URL']
				if 'username' in data['cisContext']['cisPolling']:
					voiceProxySettings.POLLING_USERNAME = data['cisContext']['cisPolling']['username']
				if 'password' in data['cisContext']['cisPolling']:
					voiceProxySettings.POLLING_PASSWORD = data['cisContext']['cisPolling']['password']
			
	if request.method == 'GET':
		state = voiceProxySettings.generateState();
	
	state = voiceProxySettings.generateState();
	
	
	resp_data =  json.dumps(state, separators=(',',':'))
	return Response(resp_data, mimetype='application/json',status=200)


#-------------- End API Methods ------------------------------







port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))