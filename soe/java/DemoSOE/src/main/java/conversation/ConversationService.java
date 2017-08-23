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

package conversation;

import java.util.logging.Level;
import java.util.logging.Logger;

import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.MultivaluedHashMap;
import javax.ws.rs.core.MultivaluedMap;

public class ConversationService {

    private static Logger log = Logger.getLogger(ConversationService.class.getName());
    
    private String _endPoint;
    private String _path;

    private String VERSION = "version";
    private final static String CONNECTION_TIMEOUT = "com.ibm.ws.jaxrs.client.connection.timeout";
    private final static String RECEIVE_TIMEOUT = "com.ibm.ws.jaxrs.client.receive.timeout";
    public final static long CONNECTION_TIMEOUT_DEFAULT = 10000; // 10 seconds
    public final static long READ_TIMEOUT_DEFAULT = 120000; // 2 min

    private final static String AUTH_HEADER_NAME = "Authorization";
    private final static String BASIC_AUTH_TOKEN = "Basic";
    private String _apiKey;
    private Client _client;
    private final static String PATH_MESSAGE = "v1/workspaces/%s/message";

    private String version = "";
    private String username = "";
    private String password = "";
    private String workspace_id = "";
    private String conversation_url = "";

    public ConversationService() {
    }

    /**
     * Initialize the Conversation variables and pass the request to
     * conversation
     * 
     * @param key
     *            The sessionID
     * @param request
     *            The request to be sent to conversation
     * @return Response returned from conversation
     */
    public MessageResponse sendToConversation(String key, MessageRequest request) {
        MessageResponse response = new MessageResponse();
        setConversationVariablesFromEnv();

        configureRestClient();
        updateConfig();
        response = sendRequest(request);

        if (response == null) {
            if (log.isLoggable(Level.WARNING)) {
                log.fine("Response from conversation is null");
            }
        }

        return response;
    }

    /**
     * Send the request to conversation and receive the response
     */
    public MessageResponse sendRequest(MessageRequest request) {

        MultivaluedMap<String, Object> headers = new MultivaluedHashMap<String, Object>();
        headers.add(AUTH_HEADER_NAME, getAuthorizationHeader());

        MessageResponse msgResponse = _client.target(_endPoint).path(_path).queryParam(VERSION, version)
                .request(MediaType.APPLICATION_JSON).headers(headers)
                .post(Entity.entity(request, MediaType.APPLICATION_JSON), MessageResponse.class);

        return msgResponse;
    }

    /**
     * @return the Authorization header field
     */
    private String getAuthorizationHeader() {
        return BASIC_AUTH_TOKEN + " " + _apiKey;
    }

    private String buildBasicAuthKey(String username, String password) {
        String usernameAndPassword = username + ":" + password;

        return java.util.Base64.getEncoder().encodeToString(usernameAndPassword.getBytes());
    }

    /**
     * Build the rest client
     */
    private void configureRestClient() {
        ClientBuilder cb = ClientBuilder.newBuilder();
        cb.register(JsonProvider.class);
        cb.property(CONNECTION_TIMEOUT, CONNECTION_TIMEOUT_DEFAULT);
        cb.property(RECEIVE_TIMEOUT, READ_TIMEOUT_DEFAULT);

        _client = cb.build();
    }

    /**
     * Connect to conversation with credentials
     */
    public void updateConfig() {
        String endPoint = conversation_url;
        if (endPoint != null) {
            _endPoint = endPoint;
        }

        String workspaceID = workspace_id;
        if (workspaceID != null) {
            _path = String.format(PATH_MESSAGE, workspaceID);
        }

        if (username != "" && password != "") {
            setRestAPIUsernameAndPassword(username, password);
        }
    }

    /**
     * Build a key for Rest API Basic authentication
     * 
     */
    private void setRestAPIUsernameAndPassword(String username, String password) {
        _apiKey = buildBasicAuthKey(username, password);
    }

    /**
     * Get the conversation variables from the env file
     */
    private void setConversationVariablesFromEnv() {
        try {
            InitialContext ic = new InitialContext();

            username = (String) ic.lookup("CONVERSATION_USERNAME");
            password = (String) ic.lookup("CONVERSATION_PASSWORD");
            version = (String) ic.lookup("CONVERSATION_VERSION");

            conversation_url = (String) ic.lookup("CONVERSATION_URL");
            workspace_id = (String) ic.lookup("WORKSPACE_ID");

        } catch (NamingException e) {
            if (log.isLoggable(Level.WARNING)) {
                log.fine("Failure to initialize env variable: " + e.getMessage());
            }
        }
    }
}
