
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
const SpeechToTextV1 = require('watson-developer-cloud/speech-to-text/v1');
const SpeechToTextEngine = require('./SpeechToTextEngine');

const Config = require('config');

const LOG_LEVEL = Config.get('LogLevel');
const logger = require('pino')({ level: LOG_LEVEL, name: 'WatsonSpeechToTextEngine' });

const WatsonSpeechToTextCredentials = Config.get('WatsonSpeechToText.credentials');
const { username } = WatsonSpeechToTextCredentials;
const { password } = WatsonSpeechToTextCredentials;

const speechToText = new SpeechToTextV1({
  username,
  password,
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

    const params = Object.assign(config, { objectMode: true });
    logger.debug('sending recognize request');

    // Watson Node-SDK supports NodeJS streams, we can return this as our stream
    // The idea is your implementation must emit 'data' events that are formatted as Watson results
    // See the WatsonSpeechToText API https://www.ibm.com/watson/developercloud/speech-to-text/api/v1/#recognize_sessionless_nonmp12
    this.recognizeStream = speechToText.createRecognizeStream(params);
    this.recognizeStream.initialize();
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
