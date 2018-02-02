# Sample Text To Speech Adapter

This sample text to speech adapter uses the Watson SDK for Text To Speech found [here](https://github.com/watson-developer-cloud/node-sdk).

## Background

By default IBM Voice Gateway uses the Watson Speech services for Text To Speech synthesis, the purpose of this project is to show how a developer can integrate a third party Text To Speech engine with IBM Voice Gateway. This project uses the Watson SDK for Text To Speech as the example for text synthesis.

## Requires
- [NodeJS v6 and higher](https://nodejs.org/en/download/)
- [IBM Voice Gateway](https://www.ibm.com/support/knowledgecenter/SS4U29/deploydocker.html) Setup

## Setup with Watson Text To Speech
1. Clone the Samples Repository
    ```
    git clone https://github.com/WASdev/sample.voice.gateway.git
    cd speech-adapter-samples/text-to-speech/
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
        "WatsonTextToSpeech": {
            "credentials": {
                "username": "<username>",
                "password": "<password>"
            }
        }
    }
    ```

    You can also set environment variables, WATSON_TTS_USERNAME and WATSON_TTS_PASSWORD like so:
    ```bash
    WATSON_TTS_USERNAME=<username> WATSON_TTS_PASSWORD=<password> npm start
    ```

1. Run the test cases to validate it's working:

    ```bash
    npm test
    ```

1. Connect the Voice Gateway to this proxy, set the `WATSON_TTS_URL` under the media.relay to point to this sample proxy
    ```
    - WATSON_TTS_URL=http://{hostname}:8010
    ```

1. Make a call

### Implement your own Text To Speech Engine

  Currently, this sample only demonstrates how to use Watson Text To Speech as the Text To Speech engine for the Voice Gateway. You can use the `lib/WatsonTextToSpeechEngine.js` as a guideline on how to implement your own Text To Speech Engine. Essentially, you'll be implementing a [Readable NodeJS Stream](http://nodejs.org/api/stream.html#stream_class_stream_readable). Once you implement your own class, you can modify the `lib/TextToSpeechAdapter.js` to `require` it.

  For example,

  ```js
  // Change to your own Text to Speech Engine implementation, you can use
  // the WatsonTextToSpeechEngine.js for guidance
  const TextToSpeechEngine = require('./WatsonTextToSpeechEngine');
  ```

  ```js
  // Uses MyTextToSpeechEngine
  const TextToSpeechEngine = require('./MyTextToSpeechEngine');
  ```

  #### Configuration
  In terms of configuration, a `config` object is passed in the constructor argument of your stream. Do note, this config object will contain Watson Text To Speech configuration items, you could map these parameters to specific parameters of your third party engine. For a list of configuration parameters for `Watson Text To Speech`, see the **Request** section of the [WebSocket API Reference](https://www.ibm.com/watson/developercloud/text-to-speech/api/v1/#wss_methods).

  Here's a sample config object:
  ```javascript
  {
    'accept': 'audio/basic', // Encoding of the audio, defaults to mulaw (pcmu) at 8kHz
    'voice': 'en-US_AllisonVoice'
  }
  ```
  ##### Dynamic Configuration through Conversation
  Similar to [dynamic configuration](https://www.ibm.com/support/knowledgecenter/SS4U29/dynamicspeech.html) of the Voice Gateway, you can also send configurations to the Sample STT Adapter from Conversation.

  Essentially, when using the `vgwActSetTTSConfig` action from Conversation, anything under the `config` object is passed through and used as the constructor argument for your stream engine.
  For example, setting this on the Watson Conversation service:

  ```json
  {
    "output": {
      "vgwAction": {
        "command": "vgwActSetTTSConfig",
        "parameters": {
          "config": {
            "voice": "en-US_AllisonVoice",
            "customProperty": "My Custom Property"
          }
        }
      }
    }
  }
  ```

  Will propagate to the `constructor` of the stream:

  ```javascript
  class MyTextToSpeechEngine {
    constructor(config) {
      // config.voice = "en-US_AllisonVoice"
      // config.customProperty = "My Custom Property"
    }
  }
  ```

  #### Sending synthesized Audio and Error Messages
  As shown in the `lib/WatsonTexToSpeechEngine.js`, to send audio in a NodeJS Stream, all you need is to call `this.push` with an audio chunk of type `Buffer`.

  ```javascript
  class MyTextToSpeechEngine {
    someMethod(synthesizedAudio) {
      this.push(synthesizedAudio); // Audio called with this.push will be sent to the Media Relay
    }
  }
  ```

  To surface error messages, you need to emit the `'error'` event with an error object:
  ```javascript
    const error = new Error('something bad happened, with the connection to my third party engine');
    this.emit('error', error);
  ```
  The sample will take care of propagating that error to the Media Relay.

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
## License

Licensed under [Apache 2.0 License](https://github.com/WASdev/sample.voice.gateway/blob/master/LICENSE)
