import os, requests, json, string, datetime, logging, time, csv

from os.path import join, dirname
from voiceProxySettings import APP_PROFILE_API

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging_comp_name = "Caller Profile API Stub"
file_name = 'callerProfile.csv'


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

def writeProfiles(profiles):
	with open(os.path.join(APP_PROFILE_API, file_name), 'w') as csvfile:
		fieldnames = ['Firstname', 'passcode','checking','savings','moneymarket','autoloan','studentloan','mortgage','autopayment','studentpayment','mortgagepayment']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for row in profiles:
			writer.writerow(row)
		csvfile.close()

def getProfileByName(name):
	profiles = readProfiles()
	profile = findProfileByFirstName(profiles, name)
	return profile
	
def updateProfile(profile):
	profiles = readProfiles()
	for ix, row in enumerate(profiles):
		if row['Firstname'] == profile['Firstname']:
			profiles[ix] = profile
	writeProfiles(profiles)

def findProfileByFirstName(profiles, firstname):
	for row in profiles:
		if row['Firstname'] == firstname:
			return row
	
	return None
	
	
def findAttrInProfile(profile,attr):
	if attr in profile:
		return profile[attr]
	return None
		
def getAccountBalance(profile, account):
	if findAttrInProfile(profile,account) and findAttrInProfile(profile,account) != '0':
		return int(findAttrInProfile(profile,account))
	else:
		return 0

def getLoanBalance(profile, loan):
	if findAttrInProfile(profile,loan) and findAttrInProfile(profile,loan) != '0':
		return int(findAttrInProfile(profile,loan))
	else:
		return 0

def hasLoanType(profile, loan):
	if findAttrInProfile(profile,loan) and findAttrInProfile(profile,loan) != '0':
		return True
	else:
		return False
		
def makePayment(profile, loan, account, amount):
	if hasLoanType(profile,loan) and getLoanBalance(profile,loan) > amount and getAccountBalance(profile,account) > amount:
		decrementAttr(profile,account,amount)
		decrementAttr(profile,loan,amount)	
		return True
	else:
		return False

def decrementAttr(profile,attr,amount):
	profile[attr] = str(int(profile[attr]) - amount)


def runTest():
	print("starting " + logging_comp_name)
	profiles = readProfiles()
	#for row in profiles:
	#	print(row['Firstname'], row['passcode'])

	profile = findProfileByFirstName(profiles, 'Olivia')
	print(profile)
	print("Passcode for Olivia: " + findAttrInProfile(profile,'passcode'))

	loan = 'auto loan'
	account = 'checking'

	print(loan + " balance is " + str(getLoanBalance(profile,loan)))
	print("Your " + account + " balance is " + str(getAccountBalance(profile,account)))

	if hasLoanType(profile,loan):
		print("You have a " + loan + " with a balance.")
		if makePayment(profile,loan,account,550):
			print("Payment Made")
		else:
			print("Payment error")
	print(profile)
	updateProfile(profile)
	profiles = readProfiles()
	for row in profiles:
		print(row)

