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
const { Duplex } = require('stream');

class SpeechToTextEngine extends Duplex {
  /* eslint-disable class-methods-use-this */
  _read() {}

  _write() {}

  /**
   * Destroys the Speech To Text Engine if a close from the other side occurs
   */
  // eslint-disable-next-line class-methods-use-this
  destroy() {
    throw new Error('not implemented');
  }
}
module.exports = SpeechToTextEngine;
