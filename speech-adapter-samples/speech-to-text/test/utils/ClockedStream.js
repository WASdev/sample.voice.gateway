
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

/**
 * Splits the stream into chunks and streams down out at a clocked rate
 * to simulate a real time transcription
 */
class ClockedStream extends Duplex {
  /**
   *
   * @param {Number} options.clockRate - Rate to clock out adata
   * @param {Number} options.size - Size of chunks clock out
   */
  constructor(options) {
    super();

    this.chunks = [];
    this.clockRate = options.clockRate || 20;
    this.chunkSize = options.size || 160;
    this.started = false;
    this.finished = false;
  }

  clock() {
    const chunk = this.chunks.shift();
    if (chunk) {
      this.push(chunk);
    } else {
      if (!this.finished && this.started) {
        this.emit('finished');
        this.finished = true;
      }
      // console.log('straeaming silence');
      this.push(Buffer.alloc(160, 0xFF));
    }
  }

  stop(callback) {
    this.push(null);
    clearInterval(this.interval);
    callback();
  }
  _read() {
    if (!this.started) {
      this.started = true;
      this.interval = setInterval(this.clock.bind(this), this.clockRate);
      this.emit('started');
    }
  }

  _write(chunk, encoding, callback) {
    let index = 0;
    let smallerChunk = chunk.slice(index, this.chunkSize);
    index = this.chunkSize;
    while (smallerChunk) {
      this.chunks.push(smallerChunk);
      if (index > chunk.length) {
        break;
      }
      smallerChunk = chunk.slice(index, index + this.chunkSize);
      index += (this.chunkSize);
    }
    return callback();
  }
}

module.exports = ClockedStream;
