
/**
* (C) Copyright IBM Corporation 2018.
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
const SpeechToTextV1 = require('ibm-watson/speech-to-text/v1');
const SpeechToTextEngine = require('./SpeechToTextEngine');
const { BasicAuthenticator, IamAuthenticator } = require('ibm-watson/auth');

const Config = require('config');
const CamelCase = require('camelcase');

const LOG_LEVEL = Config.get('LogLevel');
const logger = require('pino')({ level: LOG_LEVEL, name: 'WatsonSpeechToTextEngine' });

const WatsonSpeechToTextCredentials = Config.get('WatsonSpeechToText.credentials');
const { username, password } = WatsonSpeechToTextCredentials;
const basicAuthenticator = new BasicAuthenticator({ username, password });

const speechToText = new SpeechToTextV1({
  authenticator: basicAuthenticator,
  url: 'https://stream.watsonplatform.net/speech-to-text/api',
});

class WatsonSpeechToTextEngine extends SpeechToTextEngine {
  /**
   * Creates an instace of the WatsonSpeechToTextEngine, for a full list of config parameters
   * See https://console.bluemix.net/docs/services/speech-to-text/summary.html#summary
   * @param {Object} config - Configuration object
   * @param {String} config.model - Model to use, usually en-US_NarrowbandModel
   * @param {String} config.content-type - Content type to use, usually 'audio/basic' for mulaw
   * @returns {Transform} Returns a readable stream
   */
  constructor(config = {}) {
    super();

    /* eslint-disable no-param-reassign */
    // Convert to camelCase to fit SDK options

    const camelCaseParams = Object.keys(config).reduce((params, key) => {
      // eslint-disable-next-line
      console.log(Object.entries(config));
      params[CamelCase(key)] = config[key];
      return params;
    }, {});
    /* eslint-enable no-param-reassign */

    const params = Object.assign(camelCaseParams, { objectMode: true });
    logger.debug('sending recognize request');

    // Watson Node-SDK supports NodeJS streams, its open source you can
    // see the implementation of the recognize stream here: https://github.com/watson-developer-cloud/node-sdk/blob/master/lib/recognize-stream.ts
    // As a result, we can return recognize stream as our stream for the adapter
    // The idea is your implementation must emit 'data' events that are formatted as Watson results
    // See the WatsonSpeechToText API https://www.ibm.com/watson/developercloud/speech-to-text/api/v1/#recognize_sessionless_nonmp12
    this.recognizeStream = speechToText.recognizeUsingWebSocket(params);

    // Initializes the stream on IBM Node SDK
    this.recognizeStream.write(Buffer.alloc(1));
    this.recognizeStream.destroy = () => {
      this.recognizeStream.stop();
    };

    return this.recognizeStream;
  }
  /* eslint-disable class-methods-use-this */
  _read() {}

  _write() {}
}
module.exports = WatsonSpeechToTextEngine;
