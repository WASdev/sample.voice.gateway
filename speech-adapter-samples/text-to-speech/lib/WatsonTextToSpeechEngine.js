
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
const TextToSpeechV1 = require('ibm-watson/text-to-speech/v1');
const TextToSpeechEngine = require('./TextToSpeechEngine');
const { BasicAuthenticator } = require('ibm-watson/auth');
const Config = require('config');

const LOG_LEVEL = Config.get('LogLevel');
const logger = require('pino')({ level: LOG_LEVEL, name: 'WatsonTextToSpeechEngine' });

const WatsonTextToSpeechCredentials = Config.get('WatsonTextToSpeech.credentials');
const { username } = WatsonTextToSpeechCredentials;
const { password } = WatsonTextToSpeechCredentials;

const authenticator = new BasicAuthenticator({
  username,
  password,
});
const textToSpeech = new TextToSpeechV1({ authenticator });

const MISSING_TEXT_FIELD_ERROR = 'Text field must be defined';

class WatsonTextToSpeechEngine extends TextToSpeechEngine {
  /**
   * Creates an instace of the WatsonTextToSpeechEngine
   * @param {Object} config - Configuration object
   * @param {String} config.text - Text to synthesize
   * @param {String} [config.voice] - Voice to use
   * @param {String} config.accept - Content-type, this is usually accept/basic for mulaw
   * @returns {Transform} Returns a readable stream
   */
  constructor(config = {}) {
    super();

    if (typeof config.text === 'undefined') {
      this.emit('error', new Error(MISSING_TEXT_FIELD_ERROR));
    }

    this.destroyed = false;
    // NOTE - The Text To Speech Engine must output mulaw data
    const params = {
      text: config.text,
      voice: config.voice, // Optional voice
      accept: config.accept,
    };
    logger.debug(params, 'sending synthesize request');

    // Use the Node SDK to synthesize the audio
    textToSpeech
      .synthesize(params)
      .then((response) => {
        if (this.destroyed) {
          return;
        }
        response.result.on('data', (data) => {
          this.push(data);
        });
        response.result.on('end', () => {
          this.push(null);
        });

        response.result.emit('error', (error) => {
          this.emitError(error);
        });
      })
      .catch((err) => {
        this.emitError(err);
      });
  }

  emitError(error) {
    logger.error(error);
    this.emit('error', error);
  }
  /* eslint-disable class-methods-use-this */
  _read() {}

  destroy() {
    this.destroyed = true;
    this.push(null);
  }
}
module.exports = WatsonTextToSpeechEngine;
