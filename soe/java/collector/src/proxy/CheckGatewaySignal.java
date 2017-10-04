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

import conversation.MessageRequest;

public class CheckGatewaySignal {
    
    private VoiceProxyUtilities utilities;

    public CheckGatewaySignal() {
        utilities = new VoiceProxyUtilities();
    }

    /**
     * Check the signals coming from Voice Gateway looking for actions like
     * hangup or no input turn to respond accordingly
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


        if (utilities.containsKeyFromContext(request, VoiceProxyUtilities.GET_NAME)) {
            String name = (String) utilities.getInputValue(request, "text");
            name = name.trim();
            int index = name.indexOf(" ");
            String firstName = name;
            String lastName = "";
            if (index != -1) {
                firstName = name.substring(0, index);
                firstName = utilities.formatName(firstName);
                lastName = name.substring(index+1, name.length());
                lastName = utilities.formatName(lastName);
            }
            else{
                lastName = "...";
            }
            utilities.setKeyValueInContext(request, VoiceProxyUtilities.FIRST_NAME, firstName);
            utilities.setKeyValueInContext(request, VoiceProxyUtilities.LAST_NAME, lastName);
            utilities.removeKeyFromContext(request, VoiceProxyUtilities.GET_NAME);
        }
        
        if (utilities.containsKeyFromContext(request, VoiceProxyUtilities.GET_FIRST_NAME)) {
            String firstName = (String) utilities.getInputValue(request, "text");
            firstName = utilities.formatName(firstName);
            utilities.setKeyValueInContext(request, VoiceProxyUtilities.FIRST_NAME, firstName);
            utilities.removeKeyFromContext(request, VoiceProxyUtilities.GET_FIRST_NAME);
        }
        
        if (utilities.containsKeyFromContext(request, VoiceProxyUtilities.GET_LAST_NAME)) {
            String lastName = (String) utilities.getInputValue(request, "text");
            lastName = utilities.formatName(lastName);
            utilities.setKeyValueInContext(request, VoiceProxyUtilities.LAST_NAME, lastName);
            utilities.removeKeyFromContext(request, VoiceProxyUtilities.GET_LAST_NAME);
        }

        
        if (utilities.containsKeyFromContext(request, VoiceProxyUtilities.GET_TELEPHONE_NUMBER)) {
            String telNumber = (String) utilities.getInputValue(request, "text");
            System.out.println("Telephone number entering: " + telNumber);
            telNumber = utilities.convertNumbers(telNumber);
            telNumber = utilities.formatPhoneNumbers(telNumber);
            utilities.setKeyValueInContext(request, VoiceProxyUtilities.TELEPHONE_NUMBER, telNumber);
            utilities.removeKeyFromContext(request, VoiceProxyUtilities.GET_TELEPHONE_NUMBER);
        }
        
        if (utilities.containsKeyFromContext(request, VoiceProxyUtilities.GET_EMAIL_ADDRESS)) {
            String emailAddress = (String) utilities.getInputValue(request, "text");
            emailAddress = utilities.formatEmailAddress(emailAddress);
            utilities.setKeyValueInContext(request, VoiceProxyUtilities.EMAIL_ADDRESS, emailAddress);
            utilities.removeKeyFromContext(request, VoiceProxyUtilities.GET_EMAIL_ADDRESS);
        }  
        
        return request;
    }

    // End Check input from Gateway methods

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
