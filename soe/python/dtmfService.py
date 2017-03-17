# DTMF Checker
# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, logging, time
from flask import Flask, render_template, request, redirect, url_for
import couchdbkit
import voiceProxySettings

app = Flask(__name__)


	
logger = logging.getLogger(__name__)
server = couchdbkit.Server('https://79fca3e3-856f-4390-80be-3c805e89937c-bluemix:7e226a157bc4aeb361e9f81fa46cb4363e5da49ad37007a6dd77a64401d75353@79fca3e3-856f-4390-80be-3c805e89937c-bluemix.cloudant.com')
db = server.get_or_create_db('dtmf')


class DTMFWord(couchdbkit.Document):
	Word = couchdbkit.StringProperty()
	
	
DTMFWord.set_db(db)

@app.route('/dtmf/')
def hello(name=None):
    return render_template('dtmf.html', name=name)



@app.route('/dtmf/wordlist', methods=['GET'] )
def getWordList():
	
	wordlist = getWordList()
	
		
	return json.dumps(wordlist, separators=(',',':'))

@app.route('/dtmf/updateWord', methods=['PUT'] )
def updateWordList():
	logging.debug("Inside updateWordList")
	
	key = request.form['WordList']
	id = request.form['_id']
	# Should validate the key doesn't already exist
	doc = db[id]
	doc['Word']= key
	ndoc = Wordtag(doc)
	ndoc.save()

	wordlist = []
	wordlist = getWordList()
	return json.dumps(wordlist, separators=(',',':'))

@app.route('/dtmf/addWord', methods=['POST'] )	
def addWordList():
	logging.debug("Inside DTMF addWordList")
	logging.debug(request)
	
	key = request.form['WordList']
	
	# Need to check if the word already exists
	wt = DTMFWord(Word=key)
	wt.save()
	
	wordlist = []
	wordlist = getWordList()
	
	return json.dumps(wordlist, separators=(',',':'))
	
@app.route('/dtmf/setup', methods=['GET'] )
def doSetup():
	message = "Error in setting up the database"
	if 'start' in request.args:
		if request.args['start'] == 'true':
			wordDict = createDict()
			for wd, word in wordDict.iteritems():
				if 'Word' in word:
					logging.debug("Word is : " + word['Word'])
					wt = DTMFWord(Word=word['Word'])
					wt.save()
					time.sleep(1)
			message = "Database setup is Complete"
	
	return message

@app.route('/dtmf/decode', methods=['GET'] )
def doDecode():
	logging.debug("Request to decode")
	if 'digits' in request.args:
		logging.debug("Looking for word based on : " + request.args['digits'])	
		wordList = decode(request.args['digits'])

	return json.dumps(wordList, separators=(',',':'))

def decode(digits):
	wordList = findWordByDigits(digits)
	return wordList


def findWordByDigits(digits):
	logging.debug("FindWordsByDigits: " + digits)
	# This isn't optimal, but works for small list
	#wordList = getWordList()
	
	
	#1 digits can be 1-n in length
	#2 based on each char in the digit string convert the number to letter
	#3 create a list of possible letter combinations. List gets large are more numbers are passed
	#4 based on each letter combination see if there is a match in the wordlist using startswhith method
	letterList = []
	for count, c in enumerate(digits):
		tempMasterList = list(letterList)
		tempList = []
		letters = getLettersFromDigit(c)
		for c2, l in enumerate(letters):
			if count == 0:
				tempList.append(l)
				continue
			tempList.extend(addLetter(tempMasterList,l))
				
		letterList = list(tempList)
	
	wordList = findCandidateWords(letterList)
	
	logging.debug("Final Word list is")
	for w in wordList:
		logging.debug(w)
	
	
	return wordList

def findCandidateWords(letterList):
	subwords = []
	wordList = getWordList()
	for c, ll in enumerate(letterList):
		subwords.extend(trimWordsStartWith(ll,wordList))

	return subwords

def addLetter(list, letter):
	nlist = []
	for c, l in enumerate(list):
		nlist.append(l + letter)
	return nlist
	
def getLettersFromDigit(digit):
	digitsList = createDigitMapping()
	return digitsList[digit]


def trimWordsStartWith(letters, words):
	subwords = []
	for w, value in enumerate(words):
		wstring = value['Word']
		if wstring.lower().startswith(letters):
			subwords.append(wstring)
			
	return subwords


def getWords():
	return db.view('_all_docs')

def getWordList():
	wordlist = []
	
	if voiceProxySettings.DTMF_LOCAL_DICT_ENABLED:
		dict = createDict()
		for k, doc in dict.items():
			wordlist.append(doc)
	
	else:
		dict = getWords()
		for doc in dict:
			next = DTMFWord(doc)
			ndoc = db[next.id]
			wordlist.append(ndoc)
	
	return wordlist


def createDict():
	wordDict = {}
	wordDict['BCONAWA'] = {'Word': 'BCONAWA'}
	wordDict['DPEREZ1'] = {'Word': 'DPEREZ1'}
	wordDict['GSBRAR'] = {'Word': 'GSBRAR'}
	wordDict['ITORRES'] = {'Word': 'ITORRES'}
	wordDict['JCOSENZ'] = {'Word': 'JCOSENZ'}
	wordDict['JKWELLS'] = {'Word': 'JKWELLS'}
	wordDict['JLBYRD'] = {'Word': 'JLBYRD'}
	wordDict['JLHUDDL'] = {'Word': 'JLHUDDL'}
	wordDict['JRSMITH'] = {'Word': 'JRSMITH'}
	wordDict['LAGUERR'] = {'Word': 'LAGUERR'}
	wordDict['JRSMITH'] = {'Word': 'JRSMITH'}
	wordDict['MCARTER'] = {'Word': 'MCARTER'}
	wordDict['MIALBAR'] = {'Word': 'MIALBAR'}
	wordDict['MLKENDR'] = {'Word': 'MLKENDR'}
	wordDict['OTSCHIR'] = {'Word': 'OTSCHIR'}
	wordDict['RAANDRE'] = {'Word': 'RAANDRE'}
	wordDict['REONEAL'] = {'Word': 'REONEAL'}
	wordDict['RMOORE'] = {'Word': 'RMOORE'}
	wordDict['RPH'] = {'Word': 'RPH'}
	wordDict['RXDM'] = {'Word': 'RXDM'}
	wordDict['TEMAGAN'] = {'Word': 'TEMAGAN'}
	
	
	return wordDict

def createDigitMapping():
	digits = {}
	digits['0'] = ['']
	digits['1'] = ['']
	digits['2'] = ['a','b','c']
	digits['3'] = ['d','e','f']
	digits['4'] = ['g','h','i']
	digits['5'] = ['j','k','l']
	digits['6'] = ['m','n','o']
	digits['7'] = ['p','q','r','s']
	digits['8'] = ['t','u','v']
	digits['9'] = ['w','x','y','z']
	
	return digits
	
if __name__ == "__main__":
    app.run()
