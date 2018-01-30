# Sample Speech To Text Adapter

This sample speech to text adapter uses the Watson SDK for Speech To Text found [here](https://github.com/watson-developer-cloud/node-sdk).

## Background

By default IBM Voice Gateway uses the Watson Speech services for Speech To Text recognition, the purpose of this project is to show how a developer can integrate a third party Speech ToText engine with IBM Voice Gateway. For simplicity, the project uses the Watson SDK for Speech To Text as the example for speech recognition.

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

  Currently, this sample only demonstrates how to use Watson Speech To Text as the Speech To Text engine for the Voice Gateway. You can use the `lib/WatsonSpeechToTextEngine.js` as a guideline on how to implement your own Speech To Text Engine. Essentially, you'll be implementing a [Duplex NodeJS Stream](http://nodejs.org/api/stream.html#stream_class_stream_readable). Once you implement your own class, you can modify the `lib/SpeechToText.js` to `require` it.

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

  The idea is that the duplex stream, **must** emit 'data' events that are formatted as Watson Speech To Text results, see [here](https://www.ibm.com/watson/developercloud/speech-to-text/api/v1/#recognize_sessionless_nonmp12) for the API reference. Here is a basic example of what your stream should return:

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
