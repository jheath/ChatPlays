const tmi = require('tmi.js');
const _ = require('lodash');
const CONFIG = require('./config.json');

//// Set up the Twitch API
const twitchapi = require('./twitchapi.js');
twitchapi.init(
    {
        CONFIG
    }
);

//// Set up the Twitch Event Web Socket
const eventSocket = require('./eventSocket.js');
eventSocket.init(
    {
        CONFIG,
        twitchapi,
        onBitsRedemption,
        onChannelPointsRedeption
    }
);

//// Set up the Twitch Chat Connection
function chatConnect() {
    const client = new tmi.Client({
        channels: [ CONFIG.channel_name ]
    });
    client.connect().catch(console.error);
    client.on('message', (channel, tags, message, self) => {
        if(self) return;
        onChatMessage(message, tags);
    });
}

//// 
function main() {
    eventSocket.connect();
    chatConnect();
}


//// 
function onBitsRedemption(data) {

}

////
function onChannelPointsRedeption(data) {
    console.log('%j',data);
}

function onChatMessage(message, tags) {
    //console.log(tags);
    //console.log(message);
}


main();