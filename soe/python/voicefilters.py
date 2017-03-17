# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, sys, logging, time
import xmltodict
from HTMLParser import HTMLParser
from dtmfService import decode
import voiceProxySettings
# ------------------------------------------------
# GLOBAL VARIABLES -------------------------------
# ------------------------------------------------
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
    
# ------------------------------------------------
# FUNCTIONS --------------------------------------
# ------------------------------------------------
def response_filter(message):
	
	if 'output' in message:
		if 'text' in message['output']:
			outp = message['output']['text']
			logging.debug("Response Filtering")

			#Might need word level filtering, nothing yet
			for i, phrase in enumerate(outp):
				#logging.debug(phrase)
				outp[i] = swap_word_tags(outp[i])
		
	
			#line level filtering
			for i, phrase in enumerate(outp):
				#logging.debug(phrase)
				outp[i] = swap_html_tags(outp[i])
				outp[i] = strip_tags(outp[i])
				outp[i] = swap_word_tags(outp[i])
		
		
			#message level filtering
			outp = ssml_filter(outp)
	
			return message
		else:
			return message
	else:
		return message

# HTML Stripping code
# for the input phrase looping through the html tag list to remove from phrase
def swap_html_tags(phrase):
	tags = load_html_tags()
	nphrase = phrase
	for tg in tags:
		#logging.debug("Looking for html tag" + tg + " in\n" + nphrase)
		nphrase = nphrase.replace(tg,' ')
		#logging.debug("\n" + nphrase)
	return nphrase

def load_html_tags():
	tags = ["</br>","<href>","</href>"]
	return tags


# Word swapping
# for the input phrase looping through the word from an existing list to remove from phrase and replace with alternative
def swap_word_tags(phrase):
	tags = load_word_tags()
	nphrase = phrase
	for tg in tags:
		#logging.debug("Looking for word tag" + tg + " in\n" + nphrase)
		nphrase = nphrase.replace(tg,tags[tg])
		#logging.debug("\n" + nphrase)
	return nphrase

def load_word_tags():
	tags = {}
	tags['NO.'] = "Number"
	tags['no.'] = "Number"
	tags['No.'] = "Number"
	tags['RX'] = "Perscription"
	tags['YesNo'] = " Yes or No" 
	return tags



def cleanResponseForGateway(message):
	if 'output' in message:
		if 'text' in message['output']:
			message['output']['text'] = ssml_filter(message['output']['text'])
	
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



# SSML Code	
def set_ssml_dict():
	ssml_dict={}
	ssml_dict['.'] = " <break strength=\"strong\"></break>"
	ssml_dict[','] = " <break strength=\"medium\"></break>"
	ssml_dict["alphanumeric"] = "alpha numeric"
	return ssml_dict


def set_context_var_dict():
	cont_var_dict = {}
	cont_var_dict["rxNumber"]="ab123"
	

# swaps the string for a ssml tagged version
def check_ssml_number(str):
	if str.isdigit():
		return '<say-as interpret-as="digits">' + str +'</say-as>'
	else:
		return str

# Checks to see if there is a number that needs to be spoken as a sequence
def check_str_num(phrase):
	nphrase = phrase.split()
	
	if len(nphrase) > 1:
		for i, str in enumerate(nphrase):
			nphrase[i]= check_ssml_number(str)
	else:
		if len(nphrase) == 1:
			nphrase[0] = check_ssml_number(nphrase[0])
		
	return " ".join(nphrase)




def set_context_state_var():
	cont_state_var = {}
	cont_state_var["AA"] = "rxNumber"
	cont_state_var["AB"] = "connecusID"

		
def swap_phrase(ssml_dict,phrase):
	nphrase = phrase
	for ssml_key in ssml_dict:
		nphrase = nphrase.replace(ssml_key,ssml_dict[ssml_key])
	
	logging.debug("Swap returning " + nphrase)
	return nphrase


def check_utterance(message):
	logging.debug("Checking Utterance")
	#logging.debug(message['input']['text'])
	#need to check if one of the required values is being asked
	#Lets assume it is the connexusID which is code "AB"
	if need_connexusID(message):
		message = filter_for_connexusID(message)
		if 'context' in message:
			if 'cisDTMF' in message['context']['cisContext']:
				if message['context']['cisContext']['cisDTMF']['Error']:
					return message
		
	else:
		logging.debug("Have a connexusID")
	
		
	check_numbers(message)	
	
	return message
	
def need_connexusID(message):
	logging.debug("Checking for ConnexusID")
	if 'needConnexusID' in message['context']:
		if 'connexusID' in message['context']:
			if len(message['context']['connexusID']) < 3:
				return message['context']['needConnexusID']
	else:
		return False

def filter_for_connexusID(message):
	logging.debug("Need to filter for ConnexusID")
	logging.debug("############\n")
	logging.debug(message['input']['text'])
	
	if voiceProxySettings.DTMF_ENABLED:
		if not 'cisDTMF' in message['context']['cisContext']:
			message['context']['cisContext']['cisDTMF']={}
		
		dtmf = dtmfCheck(message)
		message['context']['cisContext']['cisDTMF'] = dtmf
		if dtmf['Error']:
			logging.debug("DTMF Error: " + dtmf['Error_Message'])	
		else:
			if len(message['context']['connexusID']) == 0:
				if dtmf['captureComplete']: 
					logging.debug('Changing text to ConnexusID: ' +  dtmf['Words'][0])
					message['input']['text'] = dtmf['Words'][0]
			
	return message
	
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
		else:
			logging.debug("Message has a word instead of a digit")
			dtmf['Error_Code'] = 3
			dtmf['Error_Message'] = 'Spoken Text when expecting DTMF digit'
			dtmf['Error'] = True
			
			if 'cisDTMF' in message['context']['cisContext']:
				if 'digits' in message['context']['cisContext']['cisDTMF']:
					dtmf['digits'] = message['context']['cisContext']['cisDTMF']['digits']
			
			
	return dtmf

def createDefaultDTMFObject():
	dtmf = {}
	dtmf['captureComplete'] = False 
	dtmf['digits'] = ''
	dtmf['Error'] = False
	dtmf['Error_Code'] = 0
	dtmf['Error_Message'] =''
	dtmf['Words'] = []
	return dtmf

def dtmfList(message):
	if 'context' in message:
		if 'cisDTMF' in message['context']['cisContext']:
			if 'digits' in message['context']['cisContext']['cisDTMF']:
				return message['context']['cisContext']['cisDTMF']['digits']
	return ""		
	
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
