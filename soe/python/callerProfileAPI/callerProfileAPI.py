import os, requests, json, string, datetime, logging, time, csv

from os.path import join, dirname



# __file__ refers to the file settings.py 

APP_PROFILE_API = os.path.dirname(os.path.abspath(__file__)) 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging_comp_name = "Caller Profile API Stub"
file_name = 'callerProfile.csv'
json_file_name = 'callerProfile.json'

def readProfiles():
	with open(os.path.join(APP_PROFILE_API, file_name), 'rb') as csvfile:
		csvprofiles = csv.DictReader(csvfile)
		profiles = []
		for row in csvprofiles:
			#print(row)
			profiles.append(row)	
		csvfile.close()
		return profiles
		
	csvfile.close()
	return None

def readCustomers():
	with open(os.path.join(APP_PROFILE_API, json_file_name), 'rb') as json_data:
		data = json.load(json_data)
	return data

def writeCustomers(customers):
	with open(os.path.join(APP_PROFILE_API, json_file_name), 'w') as outfile:
		json.dump(customers, outfile)
    
def getCustomerByName(name):
	customers = readCustomers()
	customer = findProfileByFirstName(customers, name)
	return customer
	
def updateCustomer(customer):
	customers = readCustomers()
	for ix, row in enumerate(customers):
		if 'customer' in row:
			if 'id' in row['customer'] and row['customer']['id'] == customer['customer']['id']:
				customers[ix] = customer
				writeCustomers(customers)
				return True
	return False
	

def getCustomerByID(id):
	customers = readCustomers()
	customer = findProfileByID(customers, id)
	return customer

def findProfileByFirstName(customers, firstname):
	for row in customers:
		if 'customer' in row:
			if 'Firstname' in row['customer']:
				if row['customer']['Firstname'] == firstname:
					return row
	return None

def findProfileByID(customers, id):
	for row in customers:
		if 'customer' in row and  'id' in row['customer']:
				if row['customer']['id'] == id:
					return row
	return None
	
def getAccountBalanceByName(customer, accountName):
	# looking for account by Name
	if 'accounts' in customer:
		for account in customer['accounts']:
			if 'name' in account and account['name'] == accountName:
				return account['balance']
	else:
		return 0


def getAccountBalanceByID(customer, accountID):
	# looking for account by ID
	if 'accounts' in customer:
		for account in customer['accounts']:
			if 'id' in account and account['id'] == accountID:
				return account['balance']
	
	return 0

def getAccountByID(customer, accountID):
	# looking for account by ID
	if 'accounts' in customer:
		for account in customer['accounts']:
			if 'id' in account and account['id'] == accountID:
				return account
	
	return None
	
def setAccount(customer, inaccount):
	if 'accounts' in customer:
		for ix, act in enumerate(customer['accounts']):
			if 'id' in act and act['id'] == inaccount['id']:
				customer['accounts'][ix] = inaccount

	return customer
	
def getLoanBalanceByName(customer, loanName):
	if 'loans' in customer:
		for loan in customer['loans']:
			if 'name' in loan and loan['name'] == loanName:
				return loan['balance']
	
	return 0
	
def getLoanBalanceByID(customer, loanID):
	if 'loans' in customer:
		for loan in customer['loans']:
			if 'id' in loan and loan['id'] == loanID:
				return loan['balance']
	
	return 0

def hasLoanTypeByName(customer, loanType):
	if 'loans' in customer:
		for loan in customer['loans']:
			if 'name' in loan and loan['name'] == loanType:
				return True
	
	return False

def hasLoanTypeByID(customer, loanID):
	if 'loans' in customer:
		for loan in customer['loans']:
			if 'id' in loan and loan['id'] == loanID:
				return True
	
	return False

def getLoanByID(customer, loanID):
	if 'loans' in customer:
		for loan in customer['loans']:
			if 'id' in loan and loan['id'] == loanID:
				return loan
	
	return None

def setLoan(customer, inloan):
	if 'loans' in customer:
		for ix, loan in enumerate(customer['loans']):
			if 'id' in loan and loan['id'] == inloan['id']:
				customer['loans'][ix] = inloan

	return customer

def hasCardByID(customer, cardID):
	if 'creditcards' in customer:
		for card in customer['creditcards']:
			if 'id' in card and card['id'] == cardID:
				return True
	return False

def hasCardByNum(customer, num):
	if 'creditcards' in customer:
		for card in customer['creditcards']:
			if 'cardnum' in card and card['cardnum'] == num:
				return True
	return False

def getCardByID(customer, cardID):
	if 'creditcards' in customer:
		for card in customer['creditcards']:
			if 'id' in card and card['id'] == cardID:
				return card
	return None

def getCardByNum(customer, cardNum):
	if 'creditcards' in customer:
		for card in customer['creditcards']:
			if 'cardnum' in card and card['cardnum'] == cardNum:
				return card
	return None

def getCardByName(customer, name):
	if 'creditcards' in customer:
		for card in customer['creditcards']:
			if 'name' in card and card['name'] == name:
				return card
	return None
	
def getCardBalanceByNum(customer, num):
	card = getCardByNum(customer,num)
	if card and 'balance' in card:
		return card['balance']
	
	return 0

def setCreditCard(customer, incard):
	if 'creditcards' in customer:
		for ix, card in enumerate(customer['accounts']):
			if 'id' in card and card['id'] == incard['id']:
				customer['creditcards'][ix] = incard

	return customer

def getCardBalanceByID(customer, cardID):
	if 'creditcards' in customer:
		for card in customer['creditcards']:
			if 'id' in card and card['id'] == cardID:
				return card['balance']
	
	return 0


def makeLoanPayment(profile, loan, account, amount):
	if hasLoanTypeByID(profile,loan['id']) and getLoanBalanceByID(profile,loan['id']) > amount and getAccountBalanceByID(profile,account['id']) > amount:
		loan = decrementLoan(profile,loan['id'],amount)
		setLoan(profile,loan)
		account = decrementAccount(profile,account['id'],amount)
		setAccount(profile,account)
		return True
	else:
		return False

def makeCardPayment(profile, card, account, amount):
	if hasCardByID(profile,card['id']) and getCardBalanceByNum(profile,card['id']) > amount and getAccountBalanceByID(profile,account['id']) > amount:
		loan = decrementCard(profile,card['id'],amount)
		setCreditCard(profile,loan)
		account = decrementAccount(profile,account['id'],amount)
		setAccount(profile,account)
		return True
	else:
		return False

		
def decrementAccount(customer,id,amount):
	account = getAccountByID(customer, id)
	account = decrementAccountBalance(account, amount)
	return account

def decrementAccountBalance(account, amount):
	if 'balance' in account:
		account['balance'] = account['balance'] - amount
		return account

def decrementLoan(customer,id,amount):
	loan = getLoanByID(customer, id)
	loan = decrementLoanBalance(loan, amount)
	return loan

def decrementLoanBalance(loan, amount):
	if 'balance' in loan:
		loan['balance'] = loan['balance'] - amount
	return loan

def decrementCard(customer,id,amount):
	account = getCardByID(customer, id)
	account = decrementCardBalance(account, amount)
	return account
	
def decrementCardBalance(card, amount):
	if 'balance' in card:
		card['balance'] = card['balance'] - amount
	return card
	
def runTest():
	print("starting " + logging_comp_name)
	name = 'Brian'
	profile = getCustomerByName(name)
	print(profile)
	balance = getAccountBalanceByName(profile,'checking')
	print("Checking Balance is : " + str(balance))
	
	balance = getAccountBalanceByID(profile,30)
	print("Money Market balance is :" + str(balance))
	
	if hasLoanTypeByName(profile,"studentloan"):
		print("Has studentloan")
	
	if not hasLoanTypeByName(profile,"mortgage"):
		print("doen't have mortgage")
	
	balance = getLoanBalanceByID(profile,40)
	print("Student Loand Balance is :" + str(balance))
	
	balance = getLoanBalanceByName(profile,"autoloan")
	print("Auto Loan balance is : " + str(balance))
	
	loan = getLoanByID(profile,40)
	account = getAccountByID(profile,30)
	
	print(loan)
	print(account)
	
	amount = 250
	
	print(hasLoanTypeByID(profile,loan['id']))
	print(getLoanBalanceByID(profile,loan['id']))
	print(getAccountBalanceByID(profile,account['id']))
	
	if makeLoanPayment(profile,loan,account,amount):
		print("Payment Made")
		if updateCustomer(profile):
			print(profile)
			print("Saved Payment Data")
			print("Loan Balance is: " + str(getLoanBalanceByID(profile,40)))
			print("Account Balance is: " + str(getAccountBalanceByID(profile,30)))
	else:
		print("Payment Failed")
	
	print(hasCardByNum(profile,'1357'))
	print(getCardByID(profile,'1357'))
	print(getCardBalanceByID(profile,'1357'))
	
	card = getCardByID(profile,'1357')	

	if makeCardPayment(profile,card,account,amount):
		print("Payment Made")
		if updateCustomer(profile):
			print(profile)
			print("Saved Payment Data")
			print("Card Balance is: " + str(getCardBalanceByID(profile,'1357')))
			print("Account Balance is: " + str(getAccountBalanceByID(profile,30)))
	else:
		print("Payment Failed")
	
	

#runTest()
