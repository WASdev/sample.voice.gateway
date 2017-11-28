# Tracking Latencies

Usually the most important latency metric is from when the caller finishes speaking to when he listens back from Watson. Currently there's no precise way to find out when the caller finishes speaking but you can track the time from when audio is finished playing to when Watson starts playing again.

Example conversation:

Watson: "Ok, I am back. What else would you like to learn more about the IBM Voice Gateway?"

Caller: "Let's hangup"

Watson: "<Other message>"

Identify which dialog has the latency problem, to do that look for the last utterance that Watson played before the dialog that experienced latency.

For example: "Ok, I am back. What else would you like to learn more about the IBM Voice Gateway?"

2. Search for the dialog text that Watson played in the SIP Orchestrator log file. Search for a line that contains `"CWSGW0008I: Transcription to the caller"` and the dialog text to play.

	For example:
	```
	[10/26/17 18:30:53:986 UTC] 0000008c id=         com.ibm.ws.cgw.session.FullDuplexSession                     A CWSGW0008I: Transcription to the caller aft     er modification by the plug-ins.  sessionID = 655b1470f661d5bbc4b51297c10a22fc@0.0.0.0   Transcription = Ok, I am back. What else would you like to learn m     ore about the IBM Voice Gateway?  tenantID = 18332302260¬
	```

3. Search for the next message containing `CWSGW0012I: The transaction to play text as audio completed`. Take note of the timestamp, this will be the baseline.

	For example:
	```
	[10/26/17 18:30:59:604 UTC] 0000008b id=         com.ibm.ws.cgw.session.FullDuplexSession                     A CWSGW0012I: The transaction to play text as audio completed. sessionID = 655b1470f661d5bbc4b51297c10a22fc@0.0.0.0  transactionID = c0347595-2b3f-42c6-b21f-26fe68000edb Barge-in occurred = No tenantI     D = 18332302260
	```

4. Look for the final utterance from the caller by searching for: `CWSGW0010I: Transcription from the caller. Write down the timestamp.`

	For example:
	```
	[10/26/17 18:31:02:524 UTC] 00000071 id=         com.ibm.ws.cgw.session.FullDuplexSession                     A CWSGW0010I: Transcription from the caller after modification by the plug-ins.  sessionID = 655b1470f661d5bbc4b51297c10a22fc@0.0.0.0   Transcription = let's hang up   tenantID = 18332302260
	```
5. Scroll down or search for the next term that mentions `"sendAsyncRequest:"`, for example:

	```
	[10/26/17 18:31:02:530 UTC] 00000071 id=         com.ibm.ws.cgw.conversation.conv.v1.ConversationConvImpl     1 sendAsyncRequest: send request:{"alternateI     ntents":false,"input":{"text":"let's hang up "},"context":{"email_sent":"false","system":{"dialog_stack":[{"dialog_node":"root"}],"dialog_turn_counter":6,"     dialog_request_counter":6,"_node_output_map":{"node_11_1487170755089":[0],"node_1_1505486323075":[0,1,0],"would you like to know more":[1],"how many questi     ons":[0,2,1,0],"Change voice mike":[0,1,0],"node_2_1505502966686":[0],"node_3_1505503044941":[0]},"branch_exited":true,"branch_exited_reason":"completed"},     "vgwBargeInOccurred":"No","vgwSTTResponse":{"result_index":4,"results":[{"final":true,"alternatives":[{"transcript":"let's hang up ","confidence":0.666}]}]     },"vgwPostResponseTimeoutCount":"20000","vgwTextAlternatives":"[{\"transcript\":\"let's hang up \",\"confidence\":0.666}]","conversation_id":"8a550017-2610     -4e15-a1bd-a4bd0076e6cb","vgwCompletedActions":[{"command":"vgwActUnPauseSTT","parameters":null,"processed":true},{"command":"vgwActPlayText","parameters":     {"text":["Ok, I am back. What else would you like to learn more about the IBM Voice Gateway?"]},"processed":true}],"vgwSessionID":"655b1470f661d5bbc4b51297     c10a22fc@0.0.0.0","vgwSessionInactivityTimeout":"30"}}. tenantID:18332302260. sessionID: 655b1470f661d5bbc4b51297c10a22fc@0.0.0.0¬
	```

6. Then the response form the conversation will be logged with a message: `"completed: onResponse: non null response received"`
	```
	[10/26/17 18:31:03:399 UTC] 000000e3 id=         com.ibm.ws.cgw.conversation.conv.v1.ConversationConvImpl     3 completed: onResponse: non null response re     ceived: {"entities":null,"intents":null,"input":{"text":"let's hang up "},"output":{"text":["","If you agree, we could contact you directly to provide cust     omized information for your specific application. Would you be interested and agreeable with that?"],"nodes_visited":["node_2_1495722758906","node_1_150732     6007878"],"log_messages":[]},"context":{"email_sent":"false","system":{"dialog_stack":[{"dialog_node":"node_1_1507326007878"}],"dialog_turn_counter":7,"dia     log_request_counter":7,"_node_output_map":{"node_11_1487170755089":[0],"node_1_1505486323075":[0,1,0],"would you like to know more":[1],"how many questions     ":[0,2,1,0],"Change voice mike":[0,1,0],"node_2_1505502966686":[0],"node_3_1505503044941":[0],"node_2_1495722758906":[0],"node_1_1507326007878":[0,1,0]}},"     vgwBargeInOccurred":"No","vgwSTTResponse":{"result_index":4,"results":[{"final":true,"alternatives":[{"transcript":"let's hang up ","confidence":0.666}]}]}     ,"vgwPostResponseTimeoutCount":20000,"vgwTextAlternatives":"[{\"transcript\":\"let's hang up \",\"confidence\":0.666}]","conversation_id":"8a550017-2610-4e     15-a1bd-a4bd0076e6cb","vgwSTTConfigSettings":{"config":{"model":"en-US_NarrowbandModel","profile":"low_latency","smart_formatting":true,"firmup_silence_tim     e":1}},"vgwCompletedActions":[{"command":"vgwActUnPauseSTT","parameters":null,"processed":true},{"command":"vgwActPlayText","parameters":{"text":["Ok, I am      back. What else would you like to learn more about the IBM Voice Gateway?"]},"processed":true}],"vgwSessionID":"655b1470f661d5bbc4b51297c10a22fc@0.0.0.0",     "vgwSessionInactivityTimeout":"30"},"text":["","If you agree, we could contact you directly to provide customized information for your specific application     . Would you be interested and agreeable with that?"],"vgwAction":null,"vgwActionSequence":null}. tenantID:18332302260. sessionID: 655b1470f661d5bbc4b51297c     10a22fc@0.0.0.0
	```

7. Now we want to look for the time when we send a 'playText request to the Media Relay, scroll down and look for a sendMessage log that contains "method":"playText", you want to keep note of the transactionID (unique for each playText request).

	For example:
	```
	[10/26/17 18:31:03:405 UTC] 000000bd id=         com.ibm.ws.cgw.rtprelay.impl.RTPRelaySessionImpl             3 sendMessage: {"fallbackAudioUrl":null,"method":"playText","excludeFromTTSCache":false,"text":"If you agree, we could contact you directly to provide customized information for your specific applicat     ion. Would you be interested and agreeable with that?","transactionID":"e22fb095-8b34-4538-a4df-13216636ca22","workspaceID":"b99344c6-cfe8-4399-8ff2-6bd685     d36082"}. tenantID: 18332302260. sessionID: 655b1470f661d5bbc4b51297c10a22fc@0.0.0.0¬
	```

8. Switch to the Media Relay logs, you can track the progress of a playText request by grepping the log message with the transaction ID from the previous step, for example:
	```bash
	cat trace-mr.log| grep 'e22fb095-8b34-4538-a4df-13216636ca22' > playText-e22fb095-8b34-4538-a4df-13216636ca22.log
	```

9. Open up the file "playText-e22fb095-8b34-4538-a4df-13216636ca22.log", search for the timestamp of the message "tts: connecting to Watson Text to Speech".
	For example:
	```
	[2017-10-26T18:31:03.412Z] DEBUG: RtpSessionManager/TextToSpeechStream/22 on kube-hou02-pa1901f5d258fe4e839266a298f3101a1b-w1.cloud.ibm: tts: connecting to Wats
	on Text to Speech - URI wss://<username>:<password>@stream.watsonplatform.net/text-to-speech/api/v1/synthesize?voice=en-US_MichaelVoice (sessId=655b1470f661d5bbc4b51297c10a22fc@0.0.0.0, tenantId=18332302260, transactionID=e22fb095-8b34-4538-a4df-13216636ca22)
	```

10. Search for the message that says "synthesizing audio"

	For example:
	```
	[2017-10-26T18:31:03.900Z] DEBUG: RtpSessionManager/TextToSpeechStream/22 on kube-hou02-pa1901f5d258fe4e839266a298f3101a1b-w1.cloud.ibm: synthesizing audio (sessId=655b1470f661d5bbc4b51297c10a22fc@0.0.0.0, tenantId=18332302260, transactionID=e22fb095-8b34-4538-a4df-13216636ca22)
	```


Example table filled using the steps above:
|Timestamps | Actions | Delta |
| -----------|---------|--------|
| [10/26/17 18:30:59:604 UTC] | Finished playing audio to the caller | N/A |
| [10/26/17 18:31:02:524 UTC] | Final transcription from STT | 2 seconds 920ms |
| [10/26/17 18:31:02:530 UTC] | Send request to Conversation | 6ms |
| [10/26/17 18:31:03:399 UTC] | Conversation responds with the next turn | 869ms |
| [10/26/17 18:31:03:405 UTC] | Send a request to playText to Media Relay, consequently synthesize  Text To Speech | 6ms |
| [2017-10-26T18:31:03.900Z]  | Time when we start receiving audio from Text To Speech | 495ms  |

Total Turn Latency: 4s 296ms
