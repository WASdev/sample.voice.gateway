const Config = require('config');

const PORT = Config.get('Server.port');

require('./lib/TextToSpeechAdapter').start({ port: PORT });
