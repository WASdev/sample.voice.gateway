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

package rest;

import java.util.logging.Level;
import java.util.logging.Logger;

import javax.ws.rs.Consumes;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import conversation.MessageRequest;
import conversation.MessageResponse;
import proxy.CallConversation;
import proxy.CallSystemOfRecordAfterConversation;
import proxy.CheckConversationSignal;
import proxy.CheckDTMF;
import proxy.CheckGatewaySignal;
import proxy.FromGatewayFilter;

@Path("/v1/workspaces")
public class VoiceProxyServer {
    private static Logger log = Logger.getLogger(VoiceProxyServer.class.getName());

    @POST
    @Path("/{id}/message")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    /**
     * Entry Point for messages into Voice Gateway
     */
    public MessageResponse restVoiceGatewayEntry(MessageRequest request) {
        if (log.isLoggable(Level.FINE)) {
            log.fine("------------------START OF SOE TURN-----------------");
            log.fine("\n\n\nMessage Request entering SOE: " + request.toString() + "\n\n");
        }

        // Send the request through the SOE for edits
        MessageResponse response = voiceGatewayEntry(request);

        if (response != null) {
            if (log.isLoggable(Level.FINE)) {
                log.fine("Message Response leaving SOE: " + response.toString());
                log.fine("------------------END OF SOE TURN-----------------\n\n");
            }
        }

        return response;
    }

    /**
     * Send the message request through stages both before and after it reaches
     * Watson Conversation so that changes can be made to the request or
     * response incrementally.
     * 
     * @param request
     *            The MessageRequest received from Voice Gateway headed to
     *            Conversation
     * @return MessageResponse received from Conversation and edited as needed,
     *         sent to Voice Gateway
     */
    public MessageResponse voiceGatewayEntry(MessageRequest request) {
        MessageResponse response = new MessageResponse();

        // Check the filters coming from voice gateway adding "voiceFlow"
        FromGatewayFilter fromGatewayFilter = new FromGatewayFilter();
        request = fromGatewayFilter.inputFilters(request);

        // Check the signals coming from voice gateway
        CheckGatewaySignal gatewaySignals = new CheckGatewaySignal();
        request = gatewaySignals.signals(request);

        // Check if using dtmf
        CheckDTMF checkDTMF = new CheckDTMF();
        request = checkDTMF.dtmf(request);

        // Call Watson Conversation Service
        // Switch from passing a request through methods to passing a response
        if (log.isLoggable(Level.FINE)) {
            log.fine("Message Request entering CALLCONVERSATION: " + request);
        }
        
        CallConversation callConversation = new CallConversation();
        response = callConversation.callConversationService(request);
        
        if (log.isLoggable(Level.FINE)) {
            log.fine("Message Request leaving CALLCONVERSATION: " + response + "\n\n\n");
        }

        // Check The signals from Watson Conversation
        CheckConversationSignal checkWCS = new CheckConversationSignal();
        response = checkWCS.wcsSignals(response);

        // Call the System of Records after calling the Conversation
        CallSystemOfRecordAfterConversation callSORAfter = new CallSystemOfRecordAfterConversation();
        response = callSORAfter.callSORAfterConv(response);

        return response;
    }
}