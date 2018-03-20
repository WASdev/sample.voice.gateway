
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
const TextToSpeechAdapter = require('../lib/TextToSpeechAdapter');

const HOSTNAME = 'localhost';
const PORT = 4001;

const SERVICE_URL = `http://${HOSTNAME}:${PORT}`;
const { assert } = require('chai');

describe('Text To Speech Adapter', function () {
  before(function (done) {
    TextToSpeechAdapter.start({ port: PORT })
      .then(() => (
        done()))
      .catch(done);
  });

  after(function (done) {
    TextToSpeechAdapter.stop()
      .then(() => (done()))
      .catch(done);
  });

  it('should synthesize audio', function (done) {
    this.timeout(10000);
    const ws = new WebSocket(SERVICE_URL);
    let audioDataReceivedLength = 0;
    ws.on('open', () => {
      const openingMessage = {
        accept: 'audio/basic',
        text: 'Hello World!',
      };
      ws.send(JSON.stringify(openingMessage));
    });

    ws.on('message', (data) => {
      if (typeof data === 'string') {
        done(new Error(`received non audio data: ${data.toString('utf8')}`));
      }
      audioDataReceivedLength += data.length;
    });

    ws.on('close', (code, reason) => {
      assert.equal(code, 1000, `close code should be 1000, received reason = ${reason}`);
      assert.isAbove(audioDataReceivedLength, 0, 'received 0 bytes of data');
      done();
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
