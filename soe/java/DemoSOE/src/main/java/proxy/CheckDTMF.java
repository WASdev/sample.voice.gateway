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

import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import callerProfileAPI.CallerProfile;
import callerProfileAPI.CallerProfileAPI;
import conversation.MessageRequest;

public class CheckDTMF {
    private static Logger log = Logger.getLogger(CheckDTMF.class.getName());

    
    public CheckDTMF() {
    }

    // Check DTMF Methods

    /**
     * When DTMF has been collected for the credit card, the number input must be
     * added to the database at this stage
     * 
     * @param request
     *            MessageRequest that may contain DTMF information
     * @return MessageRequest that may have been edited with DTMF information
     */
    public MessageRequest dtmf(MessageRequest request) {

        request = checkDTMF(request);
        return request;

    }

    @SuppressWarnings("unchecked")
    private MessageRequest checkDTMF(MessageRequest request) {
        if (hasDTMF(request)) {
            Map<String, Object> input = request.getInput();
            String cardNumber = (String) input.get("text");
            if (cardNumber.contains("vgwPostResponseTimeout")) {

                // DTMF Collection failed because of timeout
                input.put("text", "dtmfFailure");
                request.setInput(input);
            } else {
                // DTMF must be attempting to add a credit card .Add the card to
                // the database under the proper name, then de-identify the card
                // number
                CallerProfileAPI api = null;
                CallerProfile profile = null;
                String name = "";

                // Find the name within the response
                if (request.getContext() != null) {
                    if (request.getContext().containsKey("callerProfile")) {
                        Map<String, Object> callerProfile = (Map<String, Object>) request.getContext()
                                .get("callerProfile");
                        if (callerProfile.containsKey("firstname")) {
                            name = (String) callerProfile.get("firstname");
                        }
                    }
                }

                // Get the profile from the database based on the name
                if (name != "") {
                    api = new CallerProfileAPI();
                    profile = api.getProfileByName(name);
                }

                if (api != null) {
                    Map<String, Object> profileJson = (Map<String, Object>)request.getContext().get("profile");
                    String cardname = (String) profileJson.get("cardname");
                    if (log.isLoggable(Level.FINE)) {
                        log.fine("Attempting to add " + cardname + "with number " + cardNumber + " to " + profile);
                    }
                    api.addNewCard(profile, cardname, cardNumber);
                    api.updateProfile(profile);
                }

                // The DTMF values must be removed to protect personal
                // information. So remove them and pass along a success message
                // to conversation

                input.put("text", "dtmfSuccess");
                request.setInput(input);
                
                //Remove collectedDTMF from the context
                Map<String, Object> context = request.getContext();
                context.remove("collectedDTMF");
                request.setContext(context);
            }
        }

        return request;
    }

    private boolean hasDTMF(MessageRequest request) {
        if (request.getContext() != null) {
            if (request.getContext().containsKey("collectedDTMF")) {
                if (log.isLoggable(Level.FINE)) {
                    log.fine("DTMF digits detected");
                }
                return true;
            }
        }
        return false;
    }
}
