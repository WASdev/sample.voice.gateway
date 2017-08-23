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

import conversation.MessageRequest;

public class FromGatewayFilter {
    private static Logger log = Logger.getLogger(FromGatewayFilter.class.getName());

    
    public FromGatewayFilter() {
    }

    /**
     * Check for Voice Gateway signals that require action such as Barge-in.
     * Create any context aspects desired
     * 
     */
    public MessageRequest inputFilters(MessageRequest request) {
        request = fromGatewayFilter(request);
        return request;
    }

    /**
     * Determine sessionID for logging purposes
     */
    private MessageRequest fromGatewayFilter(MessageRequest request) {
        String sessionID = "";

        if (request.getContext() != null) {
            if (request.getContext().containsKey("vgwSessionID")) {
                sessionID = (String) request.getContext().get("vgwSessionID");
            }
        }

        // Check for a session ID
        if (sessionID != "") {
            if (log.isLoggable(Level.FINE)) {
                log.fine("API Call -> SessionID: " + sessionID);
            }
        } else {
            if (log.isLoggable(Level.WARNING)) {
                log.fine("API Call -> Serious Error, no vgwSessionID in Context");
            }
        }

        // Signal for Conversation that messages are coming from Gateway
        Map<String, Object> context = request.getContext();
        if (context != null) {
            context.put("voiceFlow", true);

            request.setContext(context);
        }

        return request;
    }
}
