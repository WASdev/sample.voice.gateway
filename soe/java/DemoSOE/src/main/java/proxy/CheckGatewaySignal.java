/**
* (C) Copyright IBM Corporation 2016.
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

import conversation.MessageRequest;

public class CheckGatewaySignal {
    
    private static Logger log = Logger.getLogger(CheckGatewaySignal.class.getName());

    public CheckGatewaySignal() {
    }

    /**
     * Check the signals coming from Voice Gateway looking for actions like if
     * there was a timeout or a hangup
     * 
     * @param request
     *            MessageRequest from Voice Gateway
     * @return MessageRequest with edits if necessary
     */
    public MessageRequest signals(MessageRequest request) {

        request = checkGatewaySignal(request);

        return request;
    }

    /**
     * Look for the signals in the Message Request, print status information and
     * set relevant settings
     * 
     */
    private MessageRequest checkGatewaySignal(MessageRequest request) {

        // Check for a timeout signal
        if (checkVGWPostResponseTimeout(request)) {
            if (log.isLoggable(Level.FINE)) {
                log.fine("Received RespTimeout message");
            }
            return request;
        }

        // Check for hangup
        if (checkVGWHangUp(request)) {
            if (log.isLoggable(Level.FINE)) {
                log.fine("Received Hangup message");
            }
            return request;
        }

        // Check for a credit card name to add to the profile
        request = checkCardName(request);

        return request;
    }

    @SuppressWarnings("unchecked")
    /**
     * The creditcard name must be added to the profile attribute. The current
     * input to the SOE is the cardname if there is the cardname attribute in
     * the profile, but the cardname attribute is still "temp"
     */
    private MessageRequest checkCardName(MessageRequest request) {
        if (request.getContext() != null) {
            Map<String, Object> context = request.getContext();
            if (context.containsKey("profile")) {
                Map<String, Object> profile = (Map<String, Object>) context.get("profile");
                if (profile.containsKey("cardname")) {
                    String cardname = (String) profile.get("cardname");
                    if (cardname.contains("temp")) {
                        // The current input text must be the cardname
                        profile.put("cardname", request.getInput().get("text"));
                        context.put("profile", profile);
                    }
                }
            }
        }

        return request;
    }

    // Signals From the SIP Gateway
    public boolean checkVGWPostResponseTimeout(MessageRequest message) {
        return checkVGWSignal(message, "vgwPostResponseTimeout");
    }

    public boolean checkVGWHangUp(MessageRequest message) {
        return checkVGWSignal(message, "vgwHangUp");
    }

    /**
     * Check for a specific signal in a message and return if it exists
     */
    public boolean checkVGWSignal(MessageRequest message, String signal) {
        if (message.getInput() != null) {
            if (message.getInput().containsKey("text")) {
                if (message.getInput().get("text").toString() == signal) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * Check for a specific signal in a message that may contain more than the
     * signal and return if it is in the
     */
    public boolean checkVGWSignalInString(MessageRequest message, String signal) {
        if (message.getInput() != null) {
            if (message.getInput().containsKey("text")) {
                if (message.getInput().get("text").toString().contains(signal)) {
                    return true;
                }
            }
        }
        return false;
    }

    // End Signals from help gateway

}
