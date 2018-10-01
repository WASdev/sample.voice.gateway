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
const WebSocketServer = require('ws').Server;

// Change to your own Speech To Text Engine implementation, you can use
// the WatsonSpeechToTextEngine.js for guidance
const SpeechToTextEngine = require('./WatsonSpeechToTextEngine');
const url = require('url');
const Config = require('config');

const DEFAULT_PORT = 8010;
const LOG_LEVEL = Config.get('LogLevel');
const logger = require('pino')({ level: LOG_LEVEL, name: 'SpeechToTextAdapter' });


function removeActiveSpeechEngine(speechToTextEngine) {
  speechToTextEngine.removeAllListeners();
  speechToTextEngine.on('error', () => {}); // no-op
  speechToTextEngine.destroy();
}

function setActiveSpeechEngine(speechToTextEngine, webSocket) {
  speechToTextEngine.on('listening', () => {
    logger.debug('engine is listening');
    const listeningMsg = {
      state: 'listening',
    };
    webSocket.send(JSON.stringify(listeningMsg));
  });
  speechToTextEngine.on('data', (sttMessage) => {
    logger.trace(sttMessage, 'result from engine:');
    if (webSocket.readyState === WebSocket.OPEN) {
      const { transcript } = sttMessage.results[0].alternatives[0];
      const { final } = sttMessage.results[0];

      if (final) {
        logger.debug(`transcript: ${transcript}`);
      }
      webSocket.send(JSON.stringify(sttMessage));
    }
  });

  speechToTextEngine.on('error', (error) => {
    logger.error(error, 'SpeechToTextEngine encountered an error: ');
    const errorMessage = {
      error: error.message,
    };

    if (webSocket.readyState === WebSocket.OPEN) {
      webSocket.send(JSON.stringify(errorMessage));
    }
  });

  speechToTextEngine.on('end', (reason = 'No close reason defined') => {
    logger.debug('SpeechToTextEngine closed');
    if (webSocket.readyState === WebSocket.OPEN) {
      webSocket.close(1000, reason);
    }
  });
}
function handleSpeechToTextConnection(webSocket, incomingMessage) {
  logger.debug('connection received');

  // Parse query parameters
  const queryParams = url.parse(incomingMessage.url, true).query;
  logger.debug(queryParams, 'query parameters:');

  // Get headers
  const { headers } = incomingMessage;
  logger.trace(headers, 'headers on websocket connection:');

  const sessionID = headers['vgw-session-id'];

  logger.debug(`connection with session-id: ${sessionID}`);
  let speechToTextEngine;
  webSocket.on('message', (data) => {
    logger.trace(data.length, 'received from websocket connection');
    if (typeof data === 'string') {
      try {
        const message = JSON.parse(data);

        if (message.action === 'start') {
          logger.debug('received: start');

          // Message contains, text and accept
          // Combine the start message with query parameters to generate a config
          const config = Object.assign(queryParams, message);
          logger.debug(config, 'config for engine: ');

          // Create a speech to text engine instance, must implement the
          // NodeJS Stream API
          speechToTextEngine = new SpeechToTextEngine(config);
          setActiveSpeechEngine(speechToTextEngine, webSocket);
        } else if (message.action === 'stop') {
          logger.debug('received: stop');
          removeActiveSpeechEngine(speechToTextEngine);
          const listeningMsg = {
            state: 'listening',
          };
          webSocket.send(JSON.stringify(listeningMsg));
        }
      } catch (e) {
        logger.error(e);
        webSocket.close(1000, 'Invalid start message');
      }
    } else if (Buffer.isBuffer(data)) {
      if (speechToTextEngine) {
        logger.trace('writing to engine');
        speechToTextEngine.write(data);
      }
    } else {
      logger.warn('received unrecognized data');
    }
  });

  // Close event
  webSocket.on('close', (code, reason) => {
    logger.debug(`onClose, code = ${code}, reason = ${reason}`);
    if (speechToTextEngine) {
      removeActiveSpeechEngine(speechToTextEngine);
    }
  });
}
let wsServer = null;

function startServer(options = { port: DEFAULT_PORT }) {
  return new Promise((resolve, reject) => {
    try {
      wsServer = new WebSocketServer({ port: options.port });
    } catch (e) {
      return reject(e);
    }

    wsServer.on('error', (error) => {
      logger.error(error);
    });

    wsServer.on('listening', () => {
      logger.info(`Speech To Text Adapter has started. Listening on port = ${options.port}`);
      resolve();
    });

    wsServer.on('connection', handleSpeechToTextConnection);
    return wsServer;
  });
}
module.exports.start = startServer;

function stopServer() {
  return new Promise((resolve, reject) => {
    if (wsServer === null) {
      return reject(new Error('server not started'));
    }
    wsServer.close((err) => {
      if (err) {
        return reject(err);
      }
      return resolve();
    });
    return wsServer;
  });
}
module.exports.stop = stopServer;

