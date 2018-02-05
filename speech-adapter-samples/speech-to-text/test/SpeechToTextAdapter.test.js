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
const WebSocket = require('ws');
const SpeechToTextAdapter = require('../lib/SpeechToTextAdapter');
const utils = require('./utils');
const URL = require('url');
const { assert } = require('chai');

const HOSTNAME = 'localhost';
const PORT = 4001;

const SERVICE_URL = `http://${HOSTNAME}:${PORT}`;

describe.only('Speech To Text Adapter', function () {
  before(function (done) {
    SpeechToTextAdapter.start({ port: PORT })
      .then(() => (
        done()))
      .catch(done);
  });

  after(function (done) {
    SpeechToTextAdapter.stop()
      .then(() => (done()))
      .catch(done);
  });

  it('should get a final result on audio', function (done) {
    this.timeout(10000);
    const queryParams = {
      model: 'en-US_NarrowbandModel',
    };
    const urlObj = URL.parse(SERVICE_URL);
    urlObj.protocol = 'ws:';
    urlObj.query = queryParams;

    const url = URL.format(urlObj);
    const realTimeAudioStream = utils.createRealTimeAudioStream('./test/resources/open_the_crate.raw');
    const ws = new WebSocket(url);
    ws.on('open', () => {
      const openingMessage = {
        action: 'start',
        'content-type': 'audio/basic',
        interim_results: true,
        inactivity_timeout: -1,
        profile: 'low_latency',
      };
      ws.send(JSON.stringify(openingMessage));
    });

    ws.on('message', (data) => {
      if (typeof data === 'string') {
        const message = JSON.parse(data);
        if (message.state === 'listening') {
          realTimeAudioStream.on('data', (audioData) => {
            // console.log(audioData.length);
            ws.send(audioData);
          });
        } else if (message.error) {
          done(new Error(message.error));
        } else {
          assert.exists(message.results);
          assert.isArray(message.results, 'Speech To Text Engine should return an array of results');
          assert.isArray(message.results[0].alternatives, 'Speech To Text Engine should return an array of results with alternatives');
          assert.isString(message.results[0].alternatives[0].transcript);

          assert.isBoolean(message.results[0].final, 'Must have a flag to indicate if it is a final result');

          const { final } = message.results[0];
          if (final) {
            done();
          }
        }
      }
    });

    ws.on('error', done);
  });

  it('should close on immediate websocket close', function (done) {
    this.timeout(10000);
    const ws = new WebSocket(SERVICE_URL);
    const audioDataReceivedLength = 0;
    ws.on('open', () => {
      const openingMessage = {
        accept: 'audio/basic',
        text: 'Hello World!',
      };
      ws.send(JSON.stringify(openingMessage));
      ws.close(1000);
    });


    ws.on('close', (code, reason) => {
      assert.equal(code, 1000, `close code should be 1000, received reason = ${reason}`);
      assert.equal(audioDataReceivedLength, 0, 'received 0 bytes of data');
      done();
    });

    ws.on('error', done);
  });
});
