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

import conversation.ConversationService;
import conversation.MessageRequest;
import conversation.MessageResponse;

public class CallConversation {

    public CallConversation() {
    }

    /**
     * Send the request to the conversation service and receive a message
     * response back
     * 
     * @param request
     *            Message request sent to Conversation
     * @return MessageResponse from Conversation
     */
    public MessageResponse callConversationService(MessageRequest request) {

        MessageResponse messageOut = new MessageResponse();
        messageOut = callConversation(request);
        return messageOut;
    }

    private MessageResponse callConversation(MessageRequest request) {
        MessageResponse messageOut = converse(request);
        return messageOut;
    }

    // Send the request with the sessionID to the conversation to obtain a
    // request
    private MessageResponse converse(MessageRequest request) {
        String sessionID = "";

        if (request.getContext() != null) {
            if (request.getContext().containsKey("vgwSessionID")) {
                sessionID = (String) request.getContext().get("vgwSessionID");
            }
        }

        if (sessionID != "") {
            ConversationService service = new ConversationService();
            return service.sendToConversation(sessionID, request);
        }
        return null;
    }

}