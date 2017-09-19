# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, sys, logging, time
import xmltodict
from HTMLParser import HTMLParser
import voiceProxySettings
# ------------------------------------------------
# GLOBAL VARIABLES -------------------------------
# ------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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
	nphrase = phrase.split()
	for ssml_key in ssml_dict:
		#nphrase = nphrase.replace(ssml_key,ssml_dict[ssml_key])
		for i, word in enumerate(nphrase):
			if '$' in word:
				continue
			if word.isdigit():
				continue
			
			nphrase[i] = word.replace(ssml_key,ssml_dict[ssml_key])
			
			
	result = " ".join(nphrase)		
	logging.debug("Swap returning " + result)
	return result