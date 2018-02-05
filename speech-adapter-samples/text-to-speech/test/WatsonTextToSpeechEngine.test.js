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
const WatsonTextToSpeechEngine = require('../lib/WatsonTextToSpeechEngine');
const { assert } = require('chai');

describe('WatsonTextToSpeechEngine', function () {
  it('should implement the stream interface', function (done) {
    this.timeout(10000);
    const config = {
      accept: 'audio/basic',
      text: 'Hello World! How can I help out with the data that is required? Will you need more assistance from me?',
    };
    const watsonTextToSpeechStream = new WatsonTextToSpeechEngine(config);

    watsonTextToSpeechStream.on('data', (data) => {
      assert.isAbove(data.length, 0);
    });
    watsonTextToSpeechStream.on('end', done);
  });

  it('should destroy the stream', function (done) {
    const config = {
      accept: 'audio/basic',
      text: 'Hello World! How can I help out with the data that is required? Will you need more assistance from me?',
    };
    const watsonTextToSpeechStream = new WatsonTextToSpeechEngine(config);
    watsonTextToSpeechStream.on('data', (data) => {
      done(new Error(`Expected no data from stream, received ${data.length}`));
    });
    watsonTextToSpeechStream.on('end', done);
    watsonTextToSpeechStream.destroy();
  });
});
