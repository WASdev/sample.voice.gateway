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
const WebSocketServer = require('ws').Server;

// Change to your own Text to Speech Engine implementation, you can use
// the WatsonTextToSpeechEngine.js for guidance
const TextToSpeechEngine = require('./WatsonTextToSpeechEngine');

const url = require('url');
const Config = require('config');

const DEFAULT_PORT = 8010;
const LOG_LEVEL = Config.get('LogLevel');
const logger = require('pino')({ level: LOG_LEVEL, name: 'TextToSpeechAdapter' });

function handleTextToSpeechConnection(webSocket, incomingMessage) {
  logger.debug('connection received');

  // Parse query parameters
  const queryParams = url.parse(incomingMessage.url, true).query;
  logger.debug(queryParams, 'query parameters:');

  // Get headers
  const { headers } = incomingMessage;
  logger.trace(headers, 'headers on websocket connection:');

  const sessionID = headers['vgw-session-id'];

  logger.debug(`connection with session-id: ${sessionID}`);
  let textToSpeechEngine;
  webSocket.on('message', (data) => {
    if (typeof data === 'string') {
      try {
        const message = JSON.parse(data);
        // Message contains, text and accept
        // Combine the start message with query parameters to generate a config
        const config = Object.assign(queryParams, message);
        logger.debug(config, 'config for engine: ');

        // Create a text to speech engine instance, must implement the
        // NodeJS Stream API
        textToSpeechEngine = new TextToSpeechEngine(config);

        textToSpeechEngine.on('data', (ttsData) => {
          logger.trace(`data from engine ${ttsData.length}`);
          webSocket.send(ttsData);
        });

        textToSpeechEngine.on('error', (error) => {
          logger.error(error, 'TextToSpeechEngine encountered an error: ');
          const errorMessage = {
            error: error.message,
          };
          webSocket.send(JSON.stringify(errorMessage));
        });

        textToSpeechEngine.on('end', (reason = 'No close reason defined') => {
          logger.debug('TextToSpeechEngine closed');
          webSocket.close(1000, reason);
        });
      } catch (e) {
        logger.error(e);
        webSocket.close(1000, 'Invalid start message');
      }
    } else {
      logger.warn('received binary data from the Media Relay');
    }
  });

  // Close event
  webSocket.on('close', (code, reason) => {
    logger.debug(`onClose, code = ${code}, reason = ${reason}`);
    if (textToSpeechEngine) {
      textToSpeechEngine.destroy();
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
      logger.info(`Text To Speech Adapter has started. Listening on port = ${options.port}`);
      resolve();
    });

    wsServer.on('connection', handleTextToSpeechConnection);
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

