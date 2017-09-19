# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time
from os.path import join, dirname
from weblogger import addLogEntry
import voiceProxySettings
from voiceProxyUtilities import check_wcsActionSignal, replaceOutputTagValue
from callerProfileAPI.callerProfileAPI import getCustomerByName, makeLoanPayment, updateCustomer, getLoanByID, getAccountByID, getCardByID, getCustomerByID
from callConversation import callConversationService
from checkConversationSignal import  wcsSignals

logging_comp_name = "callSystemOfRecordAfterConversation"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

balanceEntityTypeList = ['Accounts','Loans','Credit-Card']
balanceEntityValueList = ['Money Market','Checking','Savings','Credit Card','Auto Loan','Mortgage','Student Loan','Discover Card']

#------- Check SOR After Conversation Methods -----------------
def callSORAfterConv(message):

	message = callSystemOfRecordAfterConversation(message)
		
	return message	

def callSystemOfRecordAfterConversation(message):
	if check_wcsActionSignal(message,'getProfile'):
		logging.info("Grabing the user profile")
		message = doGetCustomer(message)
	
	if check_wcsActionSignal(message,'lookupAccountBalanceTag'):
		message = doGetCustomer(message)
		tag = '<accountBalance>'
		id = message['context']['profile']['customer']['id']
		customer = getCustomerByID(id)
		acctID =message['context']['paymentAccount']
		account = getID(customer,acctID,'accounts')
		message = replaceOutputTagValue(message,tag,account['balance'])
		return message
	
	
	
	if check_wcsActionSignal(message,'makePayment'):
		logging.info("Calling API to make a payment")
		if doMakePayment(message):
			message = doGetCustomer(message)
			if 'payment' in message['context']:
				del message['context']['payment']
	
	if check_wcsActionSignal(message,'checkBalanceAskAgain'):
		logging.info("Checking balance and Calling Conversation again based on signal")
		message['input']['text'] = message['context']['origInput']
		del message['output']
		del message['intents']
		
		
		message = doGetCustomer(message)
		message = populateBalances(message)
		message = callConversationService(message)
		message = wcsSignals(message)
		message = callSORAfterConv(message)
		
		return message
			
			
		
	return message

#------ End Check SOR After Conversation Methods ---------------

def doMakePayment(message):
	id = message['context']['profile']['Firstname']
	customer = getCustomerByName(id)
	loan = message['context']['payment']['type']
	account =message['context']['payment']['account']
	amount = message['context']['payment']['amount']
	
	loanID = getID(customer,loan,'loans')
	acctID = getID(customer,account,'accounts')
	
	 
	if makeLoanPayment(customer,loanID,acctID,amount):
		updateCustomer(customer)
		return True
		
	else:
		return False

def doGetCustomer(message):
	name = message['context']['callerProfile']['firstname']
	profile = getCustomerByName(name.strip())
	logging.info(profile['customer'])
	logging.info(profile['customer']['passcode'])
	message['context']['profile'] = profile['customer']
	return message

def getLoanID(customer, loan):
	return getID(customer,loan,'loans')
	
def getAccountID(customer, acct):
	return getID(customer,acct,'accounts')

def getCardID(customer, acct):
	return getID(customer,acct,'creditcards')
	
def getID(customer, type, list):
	if list in customer and len(customer[list])>0:
		for x in customer[list]:
			if x['name'] == type:
				return x
	
	return None	
	
def populateBalances(message):
	# need to get the name and the balances and add them to the callerProfile in the balance array
	# this is because the Watson Dialog service doesn't allow for looping through JSON arrays.
	entityBalance = loopBalanceEntities(message)
	message['context']['callerProfile']['balanceAmount'] =  entityBalance[0]['balance']
	message['context']['callerProfile']['balanceName'] =  entityBalance[0]['name']
	
	return message
	

def loopBalanceEntities(message):
	entityBalance = []
	if 'entities' in message and len(message['entities'])>0:
		for entity in message['entities']:
			if isValidBalanceEntity(entity):
				entityBalance.append(getBalanceForEntity(message,entity))
		return entityBalance
			
	return None

def isValidBalanceEntity(entity):
	if entity and entity['entity'] in balanceEntityTypeList:
		return True
	else:
		return False
	
	
def getBalanceForEntity(message,entity):
	# Need to return a list with the Entity Value and the Balance
	if entity['value'] in balanceEntityValueList:
		entityBalance = {}
		entityBalance['name'] = entity['value']
		entityBalance['balance'] = getBalanceAmount(message,entity['value'])
		return entityBalance
	return None
		
def getBalanceAmount(message,value):
	logging.info(value)
	if value == 'Money Market':
		return getBalanceFromList(message,'accounts','moneymarket')
		
	if value == 'Checking':
		return getBalanceFromList(message,'accounts','checking')
	
	if value == 'Savings':
		return getBalanceFromList(message,'accounts','savings')
	
	if value == 'Student Loan':
		return getBalanceFromList(message,'loans','studentloan')
	
	if value == 'Auto Loan':
		return getBalanceFromList(message,'loans','autoloan')
	
	if value == 'Mortgage':
		return getBalanceFromList(message,'loans','mortgage')
		
	if value == 'Discover Card':
		return getBalanceFromList(message,'creditcards','Discover')
	
	return 0
		
def getBalanceFromList(message,listname,type):
	for account in message['context']['profile'][listname]:
		if account['name'] == type:
			return account['balance']
	return None
		