# Web Based Logger
# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, logging, time, datetime
import couchdbkit
import voiceProxySettings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


CLOUDANT_URL=None


if 'CLOUDANT_URL' in os.environ:
	CLOUDANT_URL = os.environ['CLOUDANT_URL']
else:
	logging.info("No CLOUDANT_URL Defined")

if CLOUDANT_URL:	
	serverURL = CLOUDANT_URL
	databaseName ='soelogging'

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


	
def addLogEntry(app,comp, cmt, message):
	if voiceProxySettings.WEB_LOGGING and CLOUDANT_URL:
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
			logging.info("MESSAGE")
			logging.info(message)
			logging.info("END MESSAGE")
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
		logmessage=json.dumps(message, separators=(',',':'))
		logging.debug(app + " " + comp + " " + cmt + " " + logmessage)	

def getSessionLog(request):
	if CLOUDANT_URL:
		sessionID = request.form['sessionID']
	
		logging.debug("message: " +sessionID) 
	
		url = serverURL + "/" + databaseName + "/_find"
		query = createSessionTimeQuery(sessionID)
		message = postData(url,query)
		logging.info(message)
		return json.dumps(message, separators=(',',':'))
	
def getLogEntry(request):
	if CLOUDANT_URL:
		doc_id = ""
		if request.method == "POST":
			doc_id = request.form['_id']
		if request.method == "GET":
			doc_id = request.args.get('_id','')
	
		logging.debug("Doc ID: " +doc_id) 
	
		url = serverURL + "/" + databaseName + "/_find"
		query = createDocIDQuery(doc_id)
		message = postData(url,query)
		lmsg = message['docs'][0]['logmessage']
		logging.debug(lmsg)
		message['docs'][0]['logmessage'] = json.loads(lmsg)
		return json.dumps(message, separators=(',',':'))
	

def	createSessionTimeQuery(sessionID):
	query = {}
	query['selector']={}
	query['selector']['sessionID']=sessionID
	query['fields']=["_id","sessionID","logtime","comment"]
	query['sort']=[{"logtime":"asc"}]
	return query

def	createDocIDQuery(doc_id):
	query = {}
	query['selector']={}
	query['selector']['_id']=doc_id
	query['fields']=["_id","sessionID","logtime","comment","logmessage"]

	return query

def addHref(docs):
	if 'docs' in docs:
		for doc in docs['docs']:
			id = doc['_id']
			doc['_id'] = '<href="/soeLogging/getLogEntry?_id='+id+'></href>'
			
	return docs;

def getData(url):
	logging.debug(url)
	r = requests.get(url)
	message = r.json()
	return message

def postData(url,message):
	POST_SUCCESS = 200
	r = requests.post(url, headers={'content-type': 'application/json'}, data=json.dumps(message))
	logging.debug("from Post")
	logging.debug(message)
	if r.status_code == POST_SUCCESS:
		message = r.json()
	return message
