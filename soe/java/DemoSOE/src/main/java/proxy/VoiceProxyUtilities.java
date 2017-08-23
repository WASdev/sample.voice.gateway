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

import conversation.MessageResponse;

public class VoiceProxyUtilities {

    public VoiceProxyUtilities() {
    }

    /**
     * Determine if the action signal exists within the response
     */
    public boolean checkWCSActionSignal(MessageResponse response, String signal) {
        if (response.getOutput() != null) {
            if (response.getOutput().containsKey("action")) {
                String action = (String) response.getOutput().get("action");
                if (action.contains(signal)) {
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
}

