# Sample Speech To Text Adapter

This sample speech to text adapter uses the Watson SDK for Speech To Text found [here](https://github.com/watson-developer-cloud/node-sdk).

## Background

By default IBM Voice Gateway uses the Watson Speech services for Speech To Text recognition, the purpose of this project is to show how a developer can integrate a third party Speech To Text engine with IBM Voice Gateway. For simplicity, the project uses the Watson SDK for Speech To Text as the example for speech recognition.

## Requires
- [NodeJS v6 and higher](https://nodejs.org/en/download/)
- [IBM Voice Gateway](https://www.ibm.com/support/knowledgecenter/SS4U29/deploydocker.html) Setup

## Setup with Watson Speech To Text
1. Clone the Samples Repository
    ```
    git clone https://github.com/WASdev/sample.voice.gateway.git
    cd speech-adapter-samples/speech-to-text/
    ```
1. Install dependencies
    ```
    npm install
    ```
1. Add in your credentials, under `config/default.json`:
    ```json
    {
        "Server": {
            "port": 8010
        },
        "WatsonSpeechToText": {
            "credentials": {
                "username": "<username>",
                "password": "<password>"
            }
        }
    }
    ```

    You can also use environment variables, WATSON_STT_USERNAME and WATSON_STT_PASSWORD, for example:
    ```bash
    WATSON_STT_USERNAME=<username> WATSON_STT_PASSWORD=<password> npm start
    ```

1. Run the test cases to validate it's working:

    ```bash
    npm test
    ```

1. Connect the Voice Gateway to this proxy, set the `WATSON_STT_URL` under the media.relay to point to this sample proxy
    ```
    - WATSON_STT_URL=http://{hostname}:8020
    ```

1. Make a call

### Implement your own Speech To Text Engine

  Currently, this sample only demonstrates how to use Watson Speech To Text as the Speech To Text engine for the Voice Gateway. You can use the `lib/WatsonSpeechToTextEngine.js` as a guideline on how to implement your own Speech To Text Engine. Essentially, you'll be implementing a [Duplex NodeJS Stream](http://nodejs.org/api/stream.html#stream_class_stream_readable). Once you implement your own class, you can modify the `lib/SpeechToTextAdapter.js` to `require` it.

  For example,

  ```js
  // Change to your own Speech To Text Engine implementation, you can use
  // the WatsonSpeechToTextEngine.js for guidance
  const SpeechToTextEngine = require('./WatsonSpeechToTextEngine');
  ```

  ```js
  // Uses MySpeechToTextEngine
  const SpeechToTextEngine = require('./MySpeechToTextEngine');
  ```

  #### Configuration
  In terms of configuration, a `config` object is passed in the constructor argument of your stream. Do note, this config object will contain Watson Speech To Text configuration items, you could map these parameters to specific parameters of your third party engine. For a list of configuration parameters for `Watson Speech To Text`, see the **Request** section of the [WebSocket API Reference](https://www.ibm.com/watson/developercloud/speech-to-text/api/v1/#websockets).

  Here's a sample config object:
  ```javascript
  {
    'content-type': 'audio/basic', // Encoding of the audio, defaults to mulaw (pcmu) at 8kHz
    'action': 'start',            // Start message for Watson Speech To Text
    'interim_results': true,      // Receive interim results (important for triggering barge-in)
    'inactivity_timeout': -1,
    'model': 'en-US_NarrowbandModel', // Use Narrowband Model for english at 8kHZ
  }
  ```
  ##### Dynamic Configuration through Conversation
  Similar to [dynamic configuration](https://www.ibm.com/support/knowledgecenter/SS4U29/beta/speechadapter_dynamicconfig.html) the Voice Gateway STT Adapter, you can also send configurations to the Sample STT Adapter from Conversation.

  Essentially, when using the `vgwActSetSTTConfig` action from Conversation, anything under the `config` object is passed through and used as the constructor argument for your stream engine.
  For example, setting this on the Watson Conversation service:

  ```json
  {
    "output": {
      "vgwAction": {
        "command": "vgwActSetSTTConfig",
        "parameters": {
          "config": {
            "languageCode": "es-ES",
            "profanityFilter": true,
            "maxAlternatives": 2,
            "customProperty": "My Custom Property"
          }
        }
      }
  }
  ```

  Will propagate to the `constructor` of the stream:

  ```javascript
  class MySpeechToTextEngine {
    constructor(config) {
      // config.languageCode = "es-ES"
      // config.profanityFilter = true
      // config.maxAlternatives = 2
      // config.customProperty = "My Custom Property"
    }
  }
  ```
  #### Recognition results

  The idea is that the duplex stream, **must** emit 'data' events that are formatted as Watson Speech To Text results, see the **Response** section under the [WebSocket API Reference](https://www.ibm.com/watson/developercloud/speech-to-text/api/v1/#websockets)

  Here is a basic example of what your stream **must** emit on 'data' events for recognition results.

  ```json
  {
    "results": [
      {
        "alternatives": [
          {
            "transcript": "can you tell me about your menu?"
          }
        ],
        "final": true
      }
    ],
    "result_index": 0
  }
  ```

  To surface error messages, you need to emit the `'error'` event with an error object:

  ```javascript
    const error = new Error('something bad happened, with the connection to my third party engine');
    this.emit('error', error);
  ```
  The sample will take care of propagating that error to the Media Relay.

  #### Receiving Audio Data

  In your **duplex** stream the `_write` method will be called with 3 arguments,

  ```javascript
  _write(audioChunk, callback) {

    // Do something with the audio chunk

    // Always call the callback at the end to keep the flow of the stream going
    return callback();
  }
  ```

  #### Development

  To have your adapter restart on any code changes, you can run:
  ```
  npm run dev
  ```
  And it will restart the server on any file changes made.

  You can quickly test if your implementation will be compatible with the Voice Gateway, by running the `test` command:
  ```
  npm test
  ```

  Additionally, the [watson-node-sdk](https://github.com/watson-developer-cloud/node-sdk) supports NodeJS streams and it is **open source**, if you want to look into the implementation details of the stream see the [RecognizeStream.js](https://github.com/watson-developer-cloud/node-sdk/blob/master/lib/recognize-stream.ts) file.

## License

Licensed under [Apache 2.0 License](https://github.com/WASdev/sample.voice.gateway/blob/master/LICENSE)
