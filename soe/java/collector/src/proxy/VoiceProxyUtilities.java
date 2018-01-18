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

import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;

import javax.mail.Address;
import javax.mail.Message;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.AddressException;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

import conversation.MessageRequest;
import conversation.MessageResponse;

public class VoiceProxyUtilities {
    private static String SOE_CONTEXT = "soeContext";

    // action tags
    public static String GET_NAME = "getName";
    public static String GET_FIRST_NAME = "getFirstName";
    public static String GET_LAST_NAME = "getLastName";
    public static String GET_TELEPHONE_NUMBER = "getTelephoneNumber";
    public static String GET_EMAIL_ADDRESS = "getEmailAddress";
    public static String GET_EMAIL_ADDRESS_COMPLEX = "getEmailAddressComplex";
    public static String REPLACE_FIRST_NAME = "replaceFirstName";
    public static String REPLACE_LAST_NAME = "replaceLastName";
    public static String REPLACE_NAME = "replaceName";
    public static String REPLACE_TELEPHONE_NUMBER = "replaceTelephoneNumber";
    public static String REPLACE_EMAIL_ADDRESS = "replaceEmailAddress";
    public static String SEND_EMAIL_TO_REP = "sendEmailToRep";
    public static String[] statefulActionTags = { GET_NAME, GET_FIRST_NAME, GET_LAST_NAME, GET_TELEPHONE_NUMBER,
            GET_EMAIL_ADDRESS };

    // markers
    public static String REPLACE_FIRST_NAME_MARKER = "<replaceFirstName>";
    public static String REPLACE_LAST_NAME_MARKER = "<replaceLastName>";
    public static String REPLACE_NAME_MARKER = "<replaceName>";
    public static String REPLACE_TELEPHONE_NUMBER_MARKER = "<replaceTelephoneNumber>";
    public static String REPLACE_EMAIL_ADDRESS_MARKER = "<replaceEmailAddress>";

    public static String FIRST_NAME = "firstName";
    public static String LAST_NAME = "lastName";
    public static String TELEPHONE_NUMBER = "telephoneNumber";
    public static String EMAIL_ADDRESS = "emailAddress";

    public VoiceProxyUtilities() {
    }

    public String getCisAttribute(String attrib, String message) {
        return null;
    }

    public String clearCisAttribute(String attrib, String message) {
        return null;
    }

    /**
     * Determine if early return has occured in a response
     */
    @SuppressWarnings("unchecked")
    public boolean earlyReturn(MessageResponse response) {
        if (response.getContext() != null) {
            if (response.getContext().containsKey(SOE_CONTEXT)) {
                Map<String, Object> soeContext = (Map<String, Object>) response.getContext().get(SOE_CONTEXT);
                if (soeContext.containsKey("earlyReturn")) {
                    if ((Boolean) soeContext.get("earlyReturn")) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    // End Polling Helper Methods

    // Start of Checking for Conversation Signals

    /**
     * Determine if the action signal exists within the response
     */
    public boolean checkWCSActionSignal(MessageResponse response, String signal) {
        if (response.getOutput() != null) {
            if (response.getOutput().containsKey("action")) {
                String action = (String) response.getOutput().get("action");
                if (action.contains(signal)) {
                    System.out.println("Action signal detected: " + signal + "   Output: " + response.getOutput());
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * Determine if the input contains the hangup signal
     */
    public boolean checkVGWHangUp(MessageResponse response) {
        if (response.getInput() != null) {
            if (response.getInput().containsKey("text")) {
                if (response.getInput().get("text") == "vgwHangUp") {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * Remove all actions from the response output
     */
    public MessageResponse removeWCSActionSignal(MessageResponse response) {
        Map<String, Object> output = response.getOutput();
        if (output != null) {
            if (output.containsKey("action")) {
                output.remove("action");
                response.setOutput(output);
            }
        }

        return response;
    }

    /**
     * Set a value based on a key in the context of a MessageResponse
     */
    public void setKeyValueInContext(MessageResponse response, String key, Object value) {
        Map<String, Object> soeContext = null;

        if (response.getContext() != null) {
            if (response.getContext().containsKey(SOE_CONTEXT)) {
                soeContext = (Map<String, Object>) response.getContext().get(SOE_CONTEXT);
                if (soeContext.containsKey(key)) {
                    // Append the new attribute to the list of old ones

                    String attribute = (String) soeContext.get(key);
                    attribute = attribute.concat(" ");
                    attribute = attribute.concat(value.toString());
                    soeContext.put(key, attribute);
                } else {
                    // Create the attribute
                    soeContext.put(key, value);
                }
            } else {
                soeContext = new HashMap<String, Object>();
                response.getContext().put(SOE_CONTEXT, soeContext);
                soeContext.put(key, value);
            }
        }
    }

    /**
     * Set a value based on a key in the context of a MessageRequest
     */
    public void setKeyValueInContext(MessageRequest request, String key, Object value) {
        Map<String, Object> soeContext = null;
        String valueString = (String) value;

        if (request.getContext() != null) {
            if (request.getContext().containsKey(SOE_CONTEXT)) {
                soeContext = (Map<String, Object>) request.getContext().get(SOE_CONTEXT);
                if (soeContext.containsKey(key)) {
                    // Append the new attribute to the list of old ones
                    String attribute = (String) soeContext.get(key);
                    if (attribute != "") {
                        attribute = attribute.concat(" ");
                        attribute = attribute.concat(valueString);
                    }
                    soeContext.put(key, attribute);
                } else {
                    // Create the attribute
                    soeContext.put(key, value);
                }
            } else {
                soeContext = new HashMap<String, Object>();
                request.getContext().put(SOE_CONTEXT, soeContext);
                soeContext.put(key, value);
            }
        }
    }

    /**
     * Remove a value from the context of a MessageRequest based on the key
     */
    public Object removeKeyFromContext(MessageRequest request, String key) {
        Object returnValue = null;

        if (request.getContext() != null) {
            if (request.getContext().containsKey(SOE_CONTEXT)) {
                Map<String, Object> soeContext = (Map<String, Object>) request.getContext().get(SOE_CONTEXT);
                if (soeContext.containsKey(key)) {
                    returnValue = soeContext.remove(key);
                    if (soeContext.isEmpty())
                        request.getContext().remove(SOE_CONTEXT);
                }
            }
        }
        return returnValue;
    }

    /**
     * Return if the message request context contains the given key value
     */
    public boolean containsKeyFromContext(MessageRequest request, String key) {
        boolean returnValue = false;

        if (request.getContext() != null) {
            if (request.getContext().containsKey(SOE_CONTEXT)) {
                Map<String, Object> soeContext = (Map<String, Object>) request.getContext().get(SOE_CONTEXT);
                if (soeContext.containsKey(key)) {
                    returnValue = true;
                }
            }
        }
        return returnValue;
    }

    /**
     * Return the value at the given key of the input field of the message
     * request
     */
    public Object getInputValue(MessageRequest request, String key) {
        Object returnValue = false;

        if (request.getInput() != null) {
            if (request.getInput().containsKey(key)) {
                returnValue = request.getInput().get(key);
            }
        }
        return returnValue;
    }

    /**
     * Get the given key from the output field of the Message response
     */
    public Object getOutputValue(MessageResponse response, String key) {
        Object returnValue = false;

        if (response.getOutput() != null) {
            if (response.getOutput().containsKey(key)) {
                returnValue = response.getOutput().get(key);
            }
        }
        return returnValue;
    }

    /**
     * Set the given key in the output field of the message response
     */
    public void setOutputValue(MessageResponse response, String key, Object value) {

        if (response.getOutput() != null) {
            if (response.getOutput().containsKey(key)) {
                response.getOutput().put(key, value);
            }
        }
    }

    /**
     * Get the value from the given key in the context field of the message
     * response
     */
    public Object getValueFromContext(MessageResponse response, String key) {
        Object returnValue = null;

        if (response.getContext() != null) {
            if (response.getContext().containsKey(SOE_CONTEXT)) {
                Map<String, Object> soeContext = (Map<String, Object>) response.getContext().get(SOE_CONTEXT);
                if (soeContext.containsKey(key)) {
                    returnValue = soeContext.get(key);
                }
            }
        }
        return returnValue;
    }

    /**
     * Send an email to all addresses set in the server.env based on the
     * information gathered in the SOE_Context
     */
    public boolean sendEmailToRep(MessageResponse response) {
        boolean returnValue = false;

        try {
            // A MailSession is defined in the serverl.xml file. Pull the
            // mail session object from the context. It has all of the email
            // info.
            Context context = new InitialContext();
            Object sessionLookup = (Object) context.lookup("mail/ibmSMTPSession");
            Session session = (Session) sessionLookup;

            // Lookup the destination email addresses.
            InitialContext ic = new InitialContext();
            String destinationEmailAddresses = (String) ic.lookup("EMAIL_ADDRESSES");
            StringTokenizer tokenizer = new StringTokenizer(destinationEmailAddresses, ",");

            Address addressList[] = new Address[tokenizer.countTokens()];
            int i = 0;
            while (tokenizer.hasMoreTokens()) {
                addressList[i++] = new InternetAddress(tokenizer.nextToken());
            }

            Message message = new MimeMessage(session);
            message.setRecipients(Message.RecipientType.TO, addressList);
            message.setSubject("IBM VGW:   Customer followup requested");
            // System.out.println((String)getValueFromContext(response,
            // "multiple-Names"));
            if (getValueFromContext(response, "multiple-Names") != null) {
                System.out.println("Multiple names detected. Email Formatted for multiple name attempts");
                message.setText(formatEmailComplex(response));
            } else {
                message.setText(formatEmail(response));
            }
            Transport.send(message);
            returnValue = true;
        } catch (AddressException e) {
            e.printStackTrace();
        } catch (javax.mail.MessagingException e) {
            e.printStackTrace();
        } catch (NamingException e) {
            e.printStackTrace();
        }

        return returnValue;
    }

    /**
     * Get the session id from the context of a message response
     */
    private String getSessionID(MessageResponse response) {
        String returnValue = "";

        if (response.getContext() != null) {
            if (response.getContext().containsKey("vgwSessionID")) {
                returnValue = (String) response.getContext().get("vgwSessionID");
            }
        }
        return returnValue;
    }

    /**
     * Construct an email with information in the SOE_Context, formatted
     * properly
     */
    private String formatEmailComplex(MessageResponse response) {
        String email = "";

        String firstNames = (String) getValueFromContext(response, VoiceProxyUtilities.FIRST_NAME);
        String lastNames = (String) getValueFromContext(response, VoiceProxyUtilities.LAST_NAME);
        String phoneNumbers = (String) getValueFromContext(response, VoiceProxyUtilities.TELEPHONE_NUMBER);
        String emailAddress = (String) getValueFromContext(response, VoiceProxyUtilities.EMAIL_ADDRESS);

        email = "Customer Info:\n" + "First Names:    " + firstNames + "\n" + "Last Names:    " + lastNames + "\n"
                + "Telephone Numbers:    " + phoneNumbers + "\n" + "Email Addresss:    " + emailAddress + "\n"
                + "Session ID:    " + getSessionID(response) + "\n\n" + "Thanks\n";

        return email;
    }

    /**
     * Construct an email with information in the SOE_Context, formatted
     * properly
     */
    private String formatEmail(MessageResponse response) {
        String email = "";

        String firstNames = (String) getValueFromContext(response, VoiceProxyUtilities.FIRST_NAME);
        String lastNames = (String) getValueFromContext(response, VoiceProxyUtilities.LAST_NAME);
        String phoneNumbers = (String) getValueFromContext(response, VoiceProxyUtilities.TELEPHONE_NUMBER);
        String emailAddress = (String) getValueFromContext(response, VoiceProxyUtilities.EMAIL_ADDRESS);

        email = "Customer Info:\n" + "Full Names:    " + firstNames + " " + lastNames + "\n" + "Telephone Numbers:    "
                + phoneNumbers + "\n" + "Email Addresss:    " + emailAddress + "\n" + "Session ID:    "
                + getSessionID(response) + "\n\n" + "Thanks\n";

        return email;
    }

    /**
     * Convert a transcription representing a name into the proper form
     */
    public String formatName(String name) {

        // System.out.println("String entering FormatName: " + name);

        if (name != "") {

            // Resolve transcription issues, remove spacing
            name = name.toLowerCase();
            name = name.replace("\\.", "");
            name = name.replace(".", "");
            name = convertSoundsLike(name);
            name = name.replace(" ", "");
            name = name.replace("vgwpostresponsetimeout", "");
            name = name.replace("vgwhangup", "");

            // Capitalize the first letter
            if (name.length() >= 2) {
                name = name.substring(0, 1).toUpperCase() + name.substring(1);
            }
        }

        // System.out.println("String leaving FormatName: " + name);

        return name;
    }

    /**
     * Format a phone number to handle common phonetic issues
     */
    public String formatPhoneNumbers(String phoneNumbers) {

        if (phoneNumbers != "") {
            phoneNumbers = phoneNumbers.replace(" ", "");
            phoneNumbers = phoneNumbers.replace("OO", "0");
            phoneNumbers = phoneNumbers.replace("oh", "0");
            phoneNumbers = phoneNumbers.replaceAll(".*?(\\d\\s?\\d\\s?\\d\\s?(\\d\\s?)*)", "$1");
        }

        // Handle phrases for "double" and "triple" ex: double 0 = 00

        if (phoneNumbers.contains("double")) {
            String newString = "";
            String result[] = phoneNumbers.split("double");
            newString = newString.concat(result[0]);
            for (int i = 1; i < result.length; i++) {
                String temp = result[i].substring(0, 1);
                temp = temp.concat(temp);
                result[i] = temp.concat(result[i].substring(1));
                newString = newString.concat(result[i]);

            }
            phoneNumbers = newString;
        }
        if (phoneNumbers.contains("triple")) {
            String newString = "";
            String result[] = phoneNumbers.split("triple");
            newString = newString.concat(result[0]);
            for (int i = 1; i < result.length; i++) {
                String temp = result[i].substring(0, 1);
                String temp2 = temp.concat(temp);
                temp = temp.concat(temp2);
                result[i] = temp.concat(result[i].substring(1));
                newString = newString.concat(result[i]);

            }
            phoneNumbers = newString;
        }

        return phoneNumbers;
    }

    /**
     * Format an email to follow proper email construction
     */
    public String formatEmailAddress(String emails) {
        if (emails != "") {

            // Translate act and at to @
            emails = emails.replace(" at ", " @ ");
            emails = emails.replace(" dot ", " . ");
            emails = emails.replaceAll("(\\s|^)([A-Z])\\.", "$2");
            emails = phoneticMapping(emails);

            // emails = convertNumbers(emails);
            // emails = convertSoundsLike(emails);
            emails = emails.replace(" ", "");
            emails = emails.replace("vgwpostresponsetimeout", "");

            // Solve X issue
            emails = emails.replace("xyahoo", "@yahoo");
            emails = emails.replace("xgmail", "@gmail");
            emails = emails.replace("xaol", "@aol");
            emails = emails.replace("xibm", "@ibm");
            emails = emails.replace("xoutlook", "@outlook");
            emails = emails.replace("xmicrosoft", "@microsoft");
            emails = emails.replace("xicloud", "@icloud");
            emails = emails.replace("xapple", "@apple");
            emails = emails.replace("xus", "@us");
        }

        System.out.println("Email after conversion: " + emails);
        return emails;
    }

    /**
     * Convert a transcription representing a email into the relevant email
     */
    public String formatEmailAddressComplex(String emails) {

        // System.out.println("String entering FormatEmailAddress: " + emails);

        if (emails != "") {

            /// Remove spacing, resolve transcription issues, format properly
            emails = emails.replace(" act ", " @ ");
            emails = emails.replace(" at ", " @ ");
            emails = emails.replace(" dot ", " . ");
            emails = emails.replaceAll("([A-Z])\\.", "$1");
            emails = emails.toLowerCase();
            emails = phoneticMapping(emails);
            emails = convertSoundsLikeForEmail(emails);
            emails = emails.replace(" ", "");
        }

        // System.out.println("String leaving FormatEmailAddress: " + emails);

        return emails;
    }

    /**
     * Format the string to be spoken properly when read by Watson
     */
    public String formatEmailForWatson(String email) {

        // System.out.println("String entering FormatEmailForWatson: " + email);

        // . should be read as "dot" which only happens if it is isolated
        email = email.replace(".", " . ");

        // Create space between all letters and numbers to slow down the reading
        email = email.replaceAll("([a-z])", "$1. ...");
        email = email.replaceAll("([0-9])", "$1 ...");
        email = email.toUpperCase();

        // Readback common domains the way they should be read
        email = email.replace(".  G. ...O. ...V. ...", ". gov");
        email = email.replace(".  C. ...O. ...M. ...", ". com");
        email = email.replace(".  O. ...R. ...G. ...", ". org");
        email = email.replace("Y. ...A. ...H. ...O. ...O. ...", "yahoo ...");
        email = email.replace("G. ...M. ...A. ...I. ...L. ...", "G. mail ...");
        email = email.replace("M. ...I. ...C. ...R. ...O. ...S. ...O. ...F. ...T. ...", "microsoft ...");
        email = email.replace("I. ...C. ...L. ...O. ...U. ...D. ...", "I. cloud ...");
        email = email.replace("A. ...P. ...P. ...L. ...E. ...", "apple ...");
        email = email.replace("H. ...O. ...T. ...M. ...A. ...I. ...L. ...", "hot mail ... ");
        email = email.replace("O. ...U. ...T. ...L. ...O. ...O. ...K. ...", "out look ...");
        email = email.replace("I. ...N. ...B. ...O. ...X. ...", "inbox ...");
        email = email.replace("C. ...O. ...M. ...C. ...A. ...S. ...T. ...", "comcast ...");

        // Ensure that symbols are read back consistently
        email = email.replace("-", "dash ...");
        email = email.replace("_", "underscore ...");
        email = email.replace("!", "exclamation point ...");
        email = email.replace("$", "dollar sign ...");
        email = email.replace("%", "percent sign ...");
        email = email.replace("&", "ampersand ...");
        email = email.replace("*", "star ...");
        email = email.replace("#", "number sign ...");
        email = email.replace("~", "tilde ...");
        email = email.replace("?", "question mark ...");
        email = email.replace("{", "left curly bracket ...");
        email = email.replace("}", "right curly bracket ...");
        email = email.replace("/", "slash ...");
        email = email.replace("\\", "forward slash ...");
        email = email.replace("|", "vertical line ...");
        email = email.replace("'", "apostrophe ...");
        email = email.replace("+", "plus sign ...");
        email = email.replace("=", "equals sign ...");
        email = email.replace("@", "at ...");
        email = email.replace("'", "apostrophe");

        // System.out.println("String leaving FormatEmailForWatson: " + email);

        return email;
    }

    /**
     * Remove all kv pairs from the SOE_Context
     */
    public MessageResponse emptySOEContext(MessageResponse response) {
        Map<String, Object> context = response.getContext();
        if (context.containsKey(SOE_CONTEXT)) {
            context.remove(SOE_CONTEXT);
            response.setContext(context);
        }
        return response;
    }

    /**
     * Edit a string to change symbols transcribed as words into the relevant
     * symbol. Accommodates common errors E.G. "cash" = "dash"
     */
    public String phoneticMapping(String str) {

        // System.out.println("String entering PhoneticMapping: " + str);

        // Replace words for symbols with the relevant symbol
        str = str.replace("underscore", "_");
        str = str.replace("hyphen", "-");
        str = str.replace(" cash ", " dash ");
        str = str.replace("dash", "-");
        str = str.replace("exclamation mark", "!");
        str = str.replace("exclamation point", "!");
        str = str.replace("exclamation sign", "!");
        str = str.replace("exclamation", "!");
        str = str.replace("question mark", "?");
        str = str.replace("dollar sign", "$");
        str = str.replace("percent sign", "%");
        str = str.replace("percentage sign", "%");
        str = str.replace("empress and", "&");
        str = str.replace("ampersand", "&");
        str = str.replace("asterisk", "*");
        str = str.replace("star", "*");
        str = str.replace("hash sign", "#");
        str = str.replace("hash tag", "#");
        str = str.replace("hash", "#");
        str = str.replace("number sign", "#");
        str = str.replace("till date", "~");
        str = str.replace("tell day", "~");
        str = str.replace("till day", "~");
        str = str.replace("tilde", "~");
        str = str.replace("vertical line", "|");
        str = str.replace("less curly bracket", "{");
        str = str.replace("left curly bracket", "{");
        str = str.replace("right curly bracket", "}");
        str = str.replace("regularly bracket", "}");
        str = str.replace("forward slash", "/");
        str = str.replace("slash", "/");
        str = str.replace("plus sign", "+");
        str = str.replace("equals sign", "=");
        str = str.replace("apostrophe", "'");

        // Replace common domain errors with relevant domain names
        str = str.replace("jeanelle", "gmail");
        str = str.replace("g gmail", "gmail");
        str = str.replace("ggmail", "gmail");
        str = str.replace("i icloud", "icloud");
        str = str.replace("iicloud", "icloud");

        // System.out.println("String leaving PhoneticMapping: " + str);

        return str;
    }

    /**
     * Convert digits transcribed as words into proper digits including common
     * ways to say numbers E.G. two hundred becomes 200
     */
    String convertNumbers(String telNumber) {

        // System.out.println("String entering ConvertNumbers: " + telNumber);

        telNumber = telNumber.replace("zero", "0");
        telNumber = telNumber.replace("oh", "0");
        telNumber = telNumber.replaceAll("one", "1");
        telNumber = telNumber.replaceAll("two", "2");
        telNumber = telNumber.replaceAll("three", "3");
        telNumber = telNumber.replaceAll("four", "4");
        telNumber = telNumber.replaceAll("five", "5");
        telNumber = telNumber.replaceAll("six", "6");
        telNumber = telNumber.replaceAll("seven", "7");
        telNumber = telNumber.replaceAll("eight", "8");
        telNumber = telNumber.replaceAll("nine", "9");
        telNumber = telNumber.replace("hundred", "00");

        // System.out.println("String leaving ConvertNumbers: " + telNumber);

        return telNumber;
    }

    /**
     * Edits a string to accommodate spelling names using the NATO standard.
     * E.G. "A as in apple" becomes A
     */
    public String convertSoundsLike(String str) {
        // System.out.println("String entering ConvertSoundsLike: " + str);

        str = str.replaceAll("\\S+\\s(as|an|has|s|is)\\s(and)\\s*([a-z]|[A-Z])\\S*", "$3");
        // System.out.println("String after and edits: " + str);
        str = str.replaceAll("\\S+\\sas\\sin\\s*((the|a|an)\\s)*([a-z]|[A-Z])\\S*", "$3");
        // System.out.println("String after first edits: " + str);
        str = str.replaceAll("\\S+\\s(as|an|has|s|n)\\s(as|in|an|the|n|m|a|and)\\s*([a-z]|[A-Z])\\S*", "$3");
        // System.out.println("String after second edits: " + str);
        str = str.replaceAll("\\S+\\s(hasn't|doesn't|isn't)\\s([a-z]|[A-Z])\\S*", "$2");
        // System.out.println("String after third edits: " + str);
        str = str.replaceAll("artisan\\s([a-z]|[A-Z])\\S*", "$1");
        // System.out.println("String after fourth edits: " + str);
        if (!str.matches("\\S+\\s\\S+") && !str.matches("(\\S\\s)+\\S")) {
            str = str.replaceAll("\\S\\S+", "");
        }

        // System.out.println("String leaving ConvertSoundsLike: " + str);

        return str;
    }

    /**
     * Edits a string to accommodate spelling an email address using the NATO
     * standard. E.G. "A as in apple" becomes A
     */
    public String convertSoundsLikeForEmail(String str) {
        System.out.println("Email entering ConvertSoundsLikeForEmail: " + str);

        // Replace phrases containing and as a conjunction word E.G. "R s and
        // apple" = "A"
        str = str.replaceAll("^|\\S+\\s(as|an|has|s|is)\\s(and)\\s*([a-z]|[A-Z])\\S*", "$3");
        // System.out.println("String after first edits: " + str);

        // Replace phrases with excess words or misleading prefixes E.G. "T as
        // in the time" = "T"
        // "E as indoor" = "I" "R as in a pie" = "P"
        str = str.replaceAll("\\S+\\sas\\sin\\s*((the|a|an)\\s)*([a-z]|[A-Z])\\S*", "$3");
        // System.out.println("String after second edits: " + str);

        // Replace phrases with any two conjunction words E.G. "B as in boy" =
        // "B" "C has the yarn" = "Y"
        str = str.replaceAll("\\S+\\s(as|an|has|s|a)\\s(as|in|an|the|n|m|a|and)\\s*([a-z]|[A-Z])\\S*", "$3");
        // System.out.println("String after third edits: " + str);

        // Replace phrases containing conjunctions E.G. "I hasn't igloo" = "I"
        str = str.replaceAll("\\S+\\s(hasn't|doesn't|isn't)\\s([a-z]|[A-Z])\\S*", "$2");
        // System.out.println("String after fourth edits: " + str);

        // Replace phrases with single letter intermediates. E.G. "s s faster" =
        // "f" "A n apple" = "A"
        str = str.replaceAll("\\S+\\s(n|s)\\s([a-z]|[A-Z])([a-z]+|[A-Z]+)\\S*", "$2");
        // System.out.println("String after fifth edits: " + str);

        // Replace phrases with artisan E.G. "artisan run" = "R"
        str = str.replaceAll("artisan\\s([a-z]|[A-Z])\\S*", "$1");
        // System.out.println("String after sixth edits: " + str);

        // System.out.println("String before domain edits: " + str);

        // At this point, the only phrases that are not a single character or a
        // number string are either a domain name, or it should be removed

        // List of defined domains to search for, including common transcription
        // errors
        String[] domains = new String[] { "gmail", "yahoo", "ibm", "icloud", "microsoft", "outlook" };

        // Break up the transcription into chunks
        String[] tok = str.split(" ");

        // Check each chunk of the transcription
        for (int i = 0; i < tok.length; i++) {
            // System.out.println("cur token: " + tok[i]);

            // Look for chunks that are not single characters or number
            // sequences
            if (!tok[i].matches("\\s") && !tok[i].matches("[0-9]+") && !tok[i].matches("\\$[0-9]+")) {

                boolean matchesDomain = false;

                // Compare these large chunks to domain names
                for (int j = 0; j < domains.length; j++) {

                    // Remove chunks that do not match any domain names
                    if (tok[i].contains(domains[j])) {
                        // System.out.println("Found domain match: " + tok[i]);
                        matchesDomain = true;
                    }
                }
                if (!matchesDomain) {
                    tok[i] = tok[i].replaceAll("\\S\\S+", "");
                }
            }
        }

        // System.out.println(" Token at tok.length: "+ tok[tok.length - 1]);
        // for(int k = 0; k <= tok.length; k++) {
        // System.out.println("toks to be joined: " + tok[k]);
        // }

        // Bring the chunks back into a single string with chunks separated by
        // whitespaces
        str = String.join(" ", tok);

        System.out.println("Email after ConvertSoundsLikeForEmail: " + str);

        return str;
    }
}
