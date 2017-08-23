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
import conversation.MessageResponse;

public class CallSystemOfRecordAfterConversation {

    private static Logger log = Logger.getLogger(CallSystemOfRecordAfterConversation.class.getName());
    private VoiceProxyUtilities utilities;

    public CallSystemOfRecordAfterConversation() {

        utilities = new VoiceProxyUtilities();

    }

    /**
     * Make API calls based on conversation response. Interact with and update
     * the database based on conversation. Look for action signals indicating
     * how to interact with DB. This sample looks for Getting a profile or
     * making a payment for a profile
     * 
     */
    public MessageResponse callSORAfterConv(MessageResponse response) {
        response = callSystemOfRecordAfterConversation(response);
        return response;
    }

    private MessageResponse callSystemOfRecordAfterConversation(MessageResponse response) {

        //Response asks for a profile
        if (utilities.checkWCSActionSignal(response, "getProfile")) {
            if (log.isLoggable(Level.FINE)) {
                log.fine("Grabbing a user profile");
            }
            response = doGetProfile(response);
        }

        //Response wants to do a payment
        if (utilities.checkWCSActionSignal(response, "makePayment")) {
            if (log.isLoggable(Level.FINE)) {
                log.fine("Making a payment on an account");
            }
            if (doMakePayment(response)) {
                response = doGetProfile(response);
                if (response.getContext() != null) {
                    Map<String, Object> context = response.getContext();
                    if (context.containsKey("payment")) {
                        context.remove("payment");
                        response.setContext(context);
                    }
                }
            }
        }

        return response;
    }

    /**
     * Make the payment on a CallerProfile in the database
     */
    @SuppressWarnings("unchecked")
    public boolean doMakePayment(MessageResponse response) {

        String name = "";
        CallerProfile profile = null;
        String loan = "";
        String account = "";
        int amount = -1;

        // Find the name within the response
        if (response.getContext() != null) {
            if (response.getContext().containsKey("callerProfile")) {
                Map<String, Object> callerProfile = (Map<String, Object>) response.getContext().get("callerProfile");
                if (callerProfile.containsKey("firstname")) {
                    name = (String) callerProfile.get("firstname");
                }
            }
        }

        // Get the profile from the database based on the name
        if (name != "") {
            CallerProfileAPI api = new CallerProfileAPI();
            profile = api.getProfileByName(name);
        }

        // Get the payment type, account, and amount from the response
        if (response.getContext() != null) {
            if (response.getContext().containsKey("payment")) {
                Map<String, Object> payment = (Map<String, Object>) response.getContext().get("payment");
                if (payment.containsKey("type")) {
                    loan = (String) payment.get("type");
                }
                if (payment.containsKey("account")) {
                    account = (String) payment.get("account");
                }
                if (payment.containsKey("amount")) {
                    amount = (Integer) payment.get("amount");
                }
            }
        }

        // Process the payment, updating the database with the payment
        if (profile != null && account != "" && loan != "" && amount != -1) {
            CallerProfileAPI api = new CallerProfileAPI();
            if (api.makePayment(profile, loan, account, amount)) {
                api.updateProfile(profile);
                return true;
            }
        }

        return false;
    }

    /**
     * Search the csv file for a similarly named profile in the message. Then
     * replace the profile in the message with the one from the csv file.
     */
    @SuppressWarnings("unchecked")
    public MessageResponse doGetProfile(MessageResponse response) {
        String name = "";

        // Find the name within the response
        if (response.getContext() != null) {
            if (response.getContext().containsKey("callerProfile")) {
                Map<String, Object> callerProfile = (Map<String, Object>) response.getContext().get("callerProfile");
                if (callerProfile.containsKey("firstname")) {
                    name = (String) callerProfile.get("firstname");
                }
            }
        }

        // Get the profile from the database based on the name
        if (name != "") {
            CallerProfileAPI api = new CallerProfileAPI();
            CallerProfile profile = api.getProfileByName(name);
            Map<String, Object> context = response.getContext();
            context.put("profile", profile);
            response.setContext(context);
        } else {
            if (log.isLoggable(Level.FINE)) {
                log.fine("Profile not found");
            }
        }

        // return the JSONObject with the relevant profile
        return response;
    }

}
