# Web Based Logger
# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, logging, time, datetime
from flask import Flask, render_template, request, redirect, url_for
import couchdbkit
import voiceProxySettings

app = Flask(__name__)

if voiceProxySettings.WEB_LOGGING:
	if 'CLOUDANT_URL' in os.environ:
		CLOUDANT_URL = os.environ['CLOUDANT_URL']
	
	serverURL = CLOUDANT_URL
	#serverURL = 'https://79fca3e3-856f-4390-80be-3c805e89937c-bluemix:7e226a157bc4aeb361e9f81fa46cb4363e5da49ad37007a6dd77a64401d75353@79fca3e3-856f-4390-80be-3c805e89937c-bluemix.cloudant.com'
	databaseName ='soelogging'
	logger = logging.getLogger(__name__)
	server = couchdbkit.Server(serverURL)
	db = server.get_or_create_db(databaseName)


	class soeLogEntry(couchdbkit.Document):
		application = couchdbkit.StringProperty()
		sessionID = couchdbkit.StringProperty()
		logtime = couchdbkit.DateTimeProperty()
		component = couchdbkit.StringProperty()
		comment = couchdbkit.StringProperty()
		logmessage = couchdbkit.StringProperty()
		conversationid = couchdbkit.StringProperty()
		msg_input_text = couchdbkit.StringProperty()
		msg_output_text = couchdbkit.StringListProperty()
	
	
	soeLogEntry.set_db(db)

@app.route('/soeLogging/')
def hello(name=None):
    return render_template('weblogger.html', name=name)



@app.route('/soeLogging/sessionIDlist', methods=['GET'] )
def getSessionList():
	
	url = serverURL + "/" + databaseName + "/_design/logEntry/_view/sessionID-list?reduce=true&group_level=1"
	message = getData(url)
	return json.dumps(message, separators=(',',':'))

@app.route('/soeLogging/sessionLog', methods=['GET','POST'] )
def getSessionLog():
	sessionID = request.form['sessionID']
	
	logging.debug("message: " +sessionID) 
	
	url = serverURL + "/" + databaseName + "/_design/logEntry/_search/sessionID?query=sessionID:"+sessionID+"&include_docs=true"
	
	#message = postData(url,message)
	message = getData(url)
	return json.dumps(message, separators=(',',':'))


@app.route('/soeLogging/addLog', methods=['POST'] )	
def addLog():
	logging.debug("Inside soeLogging addlog")
	
	message = json.loads(request.data)
	addLogEntry(message)
	
	return json.dumps(message, separators=(',',':'))
	
def addLogEntry(app,comp, cmt, message):
	if voiceProxySettings.WEB_LOGGING:
		logging.debug("Adding Log Entry")
		conv_id = ""
		ses_id = ""
		inp = ""
		outp = ""
	
		if 'input' in message:
			if 'text' in message['input']:
				inp = message['input']['text']
	
		if 'output' in message:
			if 'text' in message['output']:
				outp = message['output']['text']
		
		if 'context' in message:
		
			if 'vgwSessionID' in message['context']:
				ses_id = message['context']['vgwSessionID']
		
			if 'conversation_id' in message['context']:
				conv_id = message['context']['conversation_id']
		
			le = soeLogEntry(sessionID=ses_id, 
			logtime=datetime.datetime.utcnow(), 
			logmessage=json.dumps(message, separators=(',',':')),
			comment=cmt, conversationid=conv_id,application=app,component=comp,
			msg_input_text = inp, msg_output_text=outp)
			le.save()	
			return
		else:
			logging.debug("No Log Entry Added... No Context Variable")	
	else:
		logging.debug(app + " " + com + " " + cmt + " " + message)i	

def getData(url):
	
	r = requests.get(url)
	message = r.json()
	return message

def postData(url,message):
	POST_SUCCESS = 200
	r = requests.post(url, headers={'content-type': 'application/json'}, data=json.dumps(message))
	if r.status_code == POST_SUCCESS:
		message = r.json()
	return message


#if __name__ == "__main__":
#    app.run()

port = os.getenv('PORT', '5001')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))