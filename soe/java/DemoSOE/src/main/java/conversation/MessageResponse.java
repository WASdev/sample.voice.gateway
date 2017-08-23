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

package conversation;

import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class MessageResponse {

    private static ObjectMapper mapper = new ObjectMapper();

    private Map<String, Object> input;
    private Map<String, Object> output;
    private Map<String, Object> context;

    public Map<String, Object> getInput() {
        return input;
    }

    public void setInput(final Map<String, Object> inputData) {
        this.input = inputData != null ? new HashMap<String, Object>(inputData) : inputData;
    }

    public Map<String, Object> getContext() {
        return context;
    }

    public void setContext(final Map<String, Object> contextData) {
        this.context = contextData != null ? new HashMap<String, Object>(contextData) : contextData;
    }

    public Map<String, Object> getOutput() {
        return output;
    }

    public void setOutput(final Map<String, Object> outputData) {
        this.output = outputData != null ? new HashMap<String, Object>(outputData) : outputData;
    }

    @Override
    public String toString() {
        return toJsonString();
    }

    public String toJsonString() {
        String jsonStr = null;
        
        try {
            jsonStr = mapper.writeValueAsString(this);
        } catch (JsonProcessingException e) {
        }
        
        return jsonStr;
    }
}
