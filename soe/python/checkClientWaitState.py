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
from voiceProxyUtilities import setEarlyReturn, earlyReturn

logging_comp_name = "checkClientWaitState"
# This is because the users wants Watson to wait until they are ready to talk again.
# Need some key words or phrase to jump out of this state.
# will need the RespTimeout Signal to be updated also.



#--- This is for the user to put Watson in a wait state ------
def waitState(message):
	message = preCheckClientWaitState(message)
	message = checkClientWaitState(message)
	message = postCheckClientWaitState(message)

	return message



def preCheckClientWaitState(message):
	return message

def checkClientWaitState(message):
	return message

def postCheckClientWaitState(message):
	return message

#------ End From Client Wait state Methods ---------------------