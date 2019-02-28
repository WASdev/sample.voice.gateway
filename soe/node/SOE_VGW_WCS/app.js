var express = require("express");
var watson = require('watson-developer-cloud');
var bodyParser = require('body-parser');

var globalContext = {};
var app = express();
var port = process.env.PORT || 8080;
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());

if (process === null || process.env === null){
	console.log("Not being able to read environment variables.");
}

var conversation = watson.conversation({
	username: process.env.wcs_username,
	password: process.env.wcs_password,
	version: 'v1',
	version_date: '2017-05-26'
});

var showAllLogs = (process.env.show_all_logs === 'true');
var receiverEmailAddress = process.env.receiver_email_address;
var senderEmailAddress = process.env.sender_email_address;
var senderEmailPassword = process.env.sender_email_password;

// code for sending mail if entities detected
function triggerMail(completeResponse) {

	var triggerMail = false;

	if (completeResponse.hasOwnProperty("intents")) {
		var intents = completeResponse.intents;
		triggerMail = true;
	}

	if (triggerMail) {
		var nodemailer = require('nodemailer');
		var transporter = nodemailer.createTransport({
			service: 'gmail',
			auth: {
				user: senderEmailAddress,
				pass: senderEmailPassword
			}
		});
		var mailOptions1 = {
				from: senderEmailAddress,
				to: receiverEmailAddress,
				subject: 'Intent detected in Conversation',
				text: 'This mail is to notify detection of Intent in Conversation.'
		};
		transporter.sendMail(mailOptions1, function(error, info){
			if (error) {
				console.log(error);
			} else {
				console.log('Email sent: ' + info.response);
			}
		});
	}
}

// change the response in this function
function editResponse(completeResponse){
	var newArray = completeResponse.output.text;
	var changedArray = [];

	// change Prosody Rate for making TTS slow 
	for (var i = 0; i < newArray.length; i++) {
		changedArray.push('<prosody rate="-9%">'+newArray[i]+'</prosody>');
	}

	var defaultVGW = [
		{
			"command": "vgwActUnPauseSTT"
		},
		{
			"command": "vgwActPlayText"
		}
		];

	// if vgwActionSequence not in response, push the default one
	if (!completeResponse.output.hasOwnProperty("vgwActionSequence")){
		completeResponse.output.vgwActionSequence = defaultVGW;
	}

	completeResponse.output.text = changedArray;
	triggerMail(completeResponse);
	return completeResponse;
}

// parent method pointing to common end point of REST call 
function commonGetPostCall(request, response) {
	var responseString = "";
	var reqBody = request.body;
	console.log("VGW to WCS, data passed through SOE is -- ");
	if (showAllLogs){
		console.log(JSON.stringify(reqBody));
	}
	else if (!showAllLogs){
		console.log(JSON.stringify(reqBody.input.text, null, 2));
	}

	reqBody.workspace_id = process.env.wcs_workspace;

	conversation.message(reqBody, function(err, response2) {
		if (err) {
			responseString += err;
		}
		else {
			var modifiedJson = editResponse(response2);
			responseString += JSON.stringify(modifiedJson, null, 2);
			if (!showAllLogs){
				console.log(JSON.stringify(modifiedJson.output.text, null, 2));
			}
		}
		console.log("WCS to VGW, data passed through SOE is -- ");
		if (showAllLogs){
			console.log(responseString);
		}
		response.end(responseString);
	});
}

app.get("/callSOE", function (request, response) {
	commonGetPostCall(request, response);
});

app.post("/callSOE", function (request, response) {
	commonGetPostCall(request, response);
});

app.listen(port);
console.log("Listening on port ", port);