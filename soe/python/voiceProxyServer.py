# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time

from os.path import join, dirname
from flask import Flask, request, render_template, redirect, url_for, Response, send_from_directory
#from weblogger import addLogEntry
from fromGatewayFilter import inputFilters
from checkGatewaySignal import signals
from checkDTMF import dtmf
from callConversation import callConversationService
from callSystemOfRecordAfterConversation import callSORAfterConv
from checkConversationSignal import wcsSignals
from toGatewayFilter import outputFilter
import voiceProxyUtilities
import voiceProxySettings
import weblogger

voiceProxySettings.init()


# ------------------------------------------------
# FLASK ------------------------------------------
# ------------------------------------------------
app = Flask(__name__)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("starting")
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

	weblogger.addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'New API Call', message)
	message = inputFilters(message)

	message = signals(message)
		
	message = callConversationService(message)
	
	message = wcsSignals(message)	
	
	message = callSORAfterConv(message)
	
	message = outputFilter(message)
	
	
	# Finally Returning to Gateway
	#weblogger.addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, 'Normal Return to Gateway', message)
	return json.dumps(message, separators=(',',':'))
	



#-------------- Gateway Utility Methods ----------------------


def earlyReturn(message):
	return voiceProxyUtilities.earlyReturn(message)
	
def returningEarlyCleanup(message, logmessage):
	earlyMsg = voiceProxyUtilities.getCisAttribute('earlyReturnMsg',message)
	if earlyMsg and len(earlyMsg)>0:
		weblogger.addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, earlyMsg, message)
		message = voiceProxyUtilities.clearCisAttribute('earlyReturn',message)
		message = voiceProxyUtilities.clearCisAttribute('earlyReturnMsg',message)
	else:
		weblogger.addLogEntry(voiceProxySettings.APP_NAME_LOGGING, logging_comp_name, logmessage, message)
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


#--------------- Web Test Client ----------------------------
@app.route('/webclient/')
def hello(name=None):
    return render_template('index.html', name=name)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)
    
@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('static/fonts', path)
    
@app.route('/api/message', methods=['POST'])
def restWebClientVoiceGatewayEntry():
	msg = json.loads(request.data)
	resp_data = voiceGatewayEntry('webclient',msg)
	return Response(resp_data, mimetype='application/json',status=200)

#-------------END Web Test Client------------------------

@app.route('/soeLogging/', methods=['GET'])
def logginghello(name=None):
    return render_template('weblogger.html', name=name)

@app.route('/jjsonviewer/<path:path>')
def send_jf(path):
    return send_from_directory('jjsonviewer/js', path)
    
@app.route('/stylesheets/<path:path>')
def send_ss(path):
    return send_from_directory('stylesheets/img', path)


@app.route('/soeLogging/sessionLog', methods=['GET','POST'] )
def getSessionLog():
	return weblogger.getSessionLog(request)

@app.route('/soeLogging/getLogEntry', methods=['GET','POST'] )
def getLogEntry():
	return weblogger.getLogEntry(request)
	






#-------------Web Logger Client -------------------------


#-------------End Web Logger Client----------------------

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))