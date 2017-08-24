/**
* (C) Copyright IBM Corporation 2017.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

package proxy;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import conversation.MessageRequest;
import conversation.MessageResponse;

public class CheckConversationSignal {

    private static Logger log = Logger.getLogger(CheckConversationSignal.class.getName());
    private VoiceProxyUtilities utilities;

    public CheckConversationSignal() {
        utilities = new VoiceProxyUtilities();
    }

    // Check Conversation Signals Methods

    /**
     * Check for actions from conversation such as requiring another call to
     * conversation if original input was not personalized to one person. Watson
     * needs to know who you are at this point if it hasn’t authenticated you.
     * This signals there may need to be cleanup or another call to conversation
     * may be needed
     * 
     */
    public MessageResponse wcsSignals(MessageResponse response) {
        response = checkConversationSignal(response);
        return response;
    }

    private MessageResponse checkConversationSignal(MessageResponse response) {

        /*
         * Almost all actions in the conversation require a login. To make the
         * flow more natural, if a question requiring login is asked, the
         * conversation will preserve the initial question before entering the
         * login process, and send the askoriginal signal when the login is
         * complete. At this point the original question, which has been saved
         * in the origInput should be treated as the input for a new request to
         * conversation
         */
        if (utilities.checkWCSActionSignal(response, "askoriginal")) {
            if (log.isLoggable(Level.FINE)) {
                log.fine("Calling conversation again with original Intent");
            }

            MessageRequest request = new MessageRequest();
            request.setContext(response.getContext());
            request.setInput(response.getInput());
            Map<String, Object> inputData = new HashMap<String, Object>();
            inputData.put("text", response.getContext().get("origInput"));
            request.setInput(inputData);

            // Call the conversation again to process the request
            CallConversation reCallConvo = new CallConversation();
            response = reCallConvo.callConversationService(request);
        }

        // Process the remaining signals
        checkWCSHangUp(response);
        response = checkCardName(response);
        response = checkDTMFSignal(response);

        return response;
    }

    /**
     * Check for a DTMF collection signal from Conversation
     */
    @SuppressWarnings("unchecked")
    public MessageResponse checkDTMFSignal(MessageResponse response) {
        if (response.getOutput() != null) {
            if (response.getOutput().containsKey("vgwAction")) {
                Map<String, Object> actionSignals = (Map<String, Object>) response.getOutput().get("vgwAction");
                if (actionSignals.containsKey("command")) {
                    if (actionSignals.get("command").toString().contains("vgwActCollectDtmf")) {
                        Map<String, Object> parameters = (Map<String, Object>) actionSignals.get("parameters");
                        if (parameters.containsKey("dtmfCount")) {
                            Map<String, Object> context = response.getContext();
                            context.put("collectedDTMF", true);
                            response.setContext(context);
                        }
                    }
                }
            }
        }

        return response;
    }

    @SuppressWarnings("unchecked")
    /**
     * Check for the action signal for collecting a cardname
     */
    public MessageResponse checkCardName(MessageResponse response) {
        if (utilities.checkWCSActionSignal(response, "cardname")) {
            Map<String, Object> context = response.getContext();
            if(context.containsKey("profile")) {
                Map<String, Object> profile = (Map<String, Object>) context.get("profile");
                profile.put("cardname", "temp");
                context.put("profile", profile);
                response.setContext(context);
            }
        }

        return response;
    }

    /**
     * Look for a hangup signal sent from conversation
     */
    public boolean checkWCSHangUp(MessageResponse response) {
        if (response.getOutput() != null) {
            if (response.getOutput().containsKey("action")) {
                return response.getOutput().get("action") == "hangup";
            }
        }
        return false;
    }
}
