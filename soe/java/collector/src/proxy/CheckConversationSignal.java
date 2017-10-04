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

import java.util.ArrayList;

import conversation.MessageResponse;

public class CheckConversationSignal {
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

        // If any of these action tags are in the response, put that state in
        // the context.
        for (int i = 0; i < VoiceProxyUtilities.statefulActionTags.length; i++) {
            if (utilities.checkWCSActionSignal(response, VoiceProxyUtilities.statefulActionTags[i])) {
                utilities.setKeyValueInContext(response, VoiceProxyUtilities.statefulActionTags[i], null);
            }
        }

        // Replace all instances of "John Doe" w/ the actual name of the
        // customer.
        if (utilities.checkWCSActionSignal(response, VoiceProxyUtilities.REPLACE_FIRST_NAME)) {
            @SuppressWarnings("unchecked")
            ArrayList<String> text = (ArrayList<String>) utilities.getOutputValue(response, "text");
            String name = (String) utilities.getValueFromContext(response, VoiceProxyUtilities.FIRST_NAME);
            String firstName = name.substring(name.lastIndexOf(" ") + 1);
            firstName = utilities.formatName(firstName);
            System.out.println("text = " + text + "    firstName = " + firstName);
            text.set(0, ((String) text.get(0)).replaceAll(VoiceProxyUtilities.REPLACE_FIRST_NAME_MARKER, firstName));
            System.out.println("text = " + text);
        }

        // Replace all instances of "John Doe" w/ the actual name of the
        // customer.
        if (utilities.checkWCSActionSignal(response, VoiceProxyUtilities.REPLACE_LAST_NAME)) {
            @SuppressWarnings("unchecked")
            ArrayList<String> text = (ArrayList<String>) utilities.getOutputValue(response, "text");
            String name = (String) utilities.getValueFromContext(response, VoiceProxyUtilities.LAST_NAME);
            String lastName = "";
            lastName = name.substring(name.lastIndexOf(" ") + 1);
            lastName = utilities.formatName(lastName);
            System.out.println("text = " + text + "    lastName = " + lastName);
            text.set(0, ((String) text.get(0)).replaceAll(VoiceProxyUtilities.REPLACE_LAST_NAME_MARKER, lastName));
            System.out.println("text = " + text);
        }

        // Replace all instances of "John Doe" w/ the actual name of the
        // customer.
        if (utilities.checkWCSActionSignal(response, VoiceProxyUtilities.REPLACE_NAME)) {
            @SuppressWarnings("unchecked")
            ArrayList<String> text = (ArrayList<String>) utilities.getOutputValue(response, "text");
            String name = (String) utilities.getValueFromContext(response, VoiceProxyUtilities.FIRST_NAME);
            name = name.split(",")[0];
            name += " ... " + (String) utilities.getValueFromContext(response, VoiceProxyUtilities.LAST_NAME);
            System.out.println("text = " + text + "    name = " + name);
            text.set(0, ((String) text.get(0)).replaceAll(VoiceProxyUtilities.REPLACE_NAME_MARKER, name));
            System.out.println("text = " + text);
        }

        // Replace all instances of "John Doe" w/ the actual name of the
        // customer.
        if (utilities.checkWCSActionSignal(response, VoiceProxyUtilities.REPLACE_TELEPHONE_NUMBER)) {
            @SuppressWarnings("unchecked")
            ArrayList<String> text = (ArrayList<String>) utilities.getOutputValue(response, "text");
            String telNumber = (String) utilities.getValueFromContext(response, VoiceProxyUtilities.TELEPHONE_NUMBER);
            String tempTelNumber = "";
            tempTelNumber = telNumber.substring(telNumber.lastIndexOf(" ") + 1);
            System.out.println("text = " + text + "    telNumber = " + tempTelNumber);
            String formattedTelNumber = "";

            for (int i = 0; i < tempTelNumber.length(); i++) {
                formattedTelNumber += " " + tempTelNumber.charAt(i);

                // After the 3rd digit (area code), add a pause "...".
                if (i == 2)
                    formattedTelNumber += "... ";
            }
            text.set(0, ((String) text.get(0)).replaceAll(VoiceProxyUtilities.REPLACE_TELEPHONE_NUMBER_MARKER,
                    formattedTelNumber));
            System.out.println("text = " + text);
        }

        // Replace all instances of "John Doe" w/ the actual name of the
        // customer.
        if (utilities.checkWCSActionSignal(response, VoiceProxyUtilities.REPLACE_EMAIL_ADDRESS)) {
            @SuppressWarnings("unchecked")
            ArrayList<String> text = (ArrayList<String>) utilities.getOutputValue(response, "text");
            String emailIn = (String) utilities.getValueFromContext(response, VoiceProxyUtilities.EMAIL_ADDRESS);
            String emailAddress = "";
            emailAddress = emailIn.substring(emailIn.lastIndexOf(" ") + 1);
            emailAddress = utilities.formatEmailForWatson(emailAddress);
            System.out.println("text = " + text + "    emailAddress = " + emailAddress);
            text.set(0,
                    ((String) text.get(0)).replaceAll(VoiceProxyUtilities.REPLACE_EMAIL_ADDRESS_MARKER, emailAddress));
            System.out.println("text = " + text);
        }

        // Replace all instances of "John Doe" w/ the actual name of the
        // customer.
        if (utilities.checkWCSActionSignal(response, VoiceProxyUtilities.SEND_EMAIL_TO_REP)) {
            utilities.sendEmailToRep(response);
            
            //Empty the SOEContext after an email is sent
            response = utilities.emptySOEContext(response);
        }

        return response;
    }
}
