var WebSocketClient = require('websocket').client;
var _ = require('lodash');

var client = new WebSocketClient();
var SESSIONID;

client.on('connectFailed', function(error) {
    console.log('Connect Error: ' + error.toString());
});

client.on('connect', function(connection) {
    console.log('WebSocket Client Connected');

    ///// TODO: FIX CONNECTION ISSUES
    connection.on('error', function(error) {
        console.log("Connection Error: " + error.toString());
    });

    ///// TODO: FIX CONNECTION ISSUES
    connection.on('close', function() {
        console.log('echo-protocol Connection Closed');
    });

    connection.on('message', function(message) {
        //// I'm not sure what else this could be....
        if (message.type === 'utf8') {
            let data = JSON.parse(message.utf8Data);

            //// We get message! Let's figure out what to do
            if (_.get(data, 'metadata.message_type') === 'session_welcome') {
                //// We're connected. Now lets save the SESSSIONID and sub to the channels we need
                SESSIONID = data.payload.session.id;
                subscribe();
            }
            else if (_.get(data, 'metadata.subscription_type') === 'channel.channel_points_automatic_reward_redemption.add') {
                //// Twitch auto-supplied channel points redemption
                settings.onChannelPointsRedeption(data);
            }
            else if (_.get(data, 'metadata.subscription_type') === 'channel.channel_points_custom_reward_redemption.add') {
                //// Custom channel points redemption
                settings.onChannelPointsRedeption(data);
            }
            else if (_.get(data, 'metadata.subscription_type') === 'channel.cheer') {
                //// Bits redemption
                settings.onBitsRedemption(data);
            }
            else if (_.get(data, 'metadata.message_type') === 'session_keepalive') {
                //// This is just the PING message we get every 30 seconds. Could be useful to keep track of
                ////    if we're worried about getting disconnected.
                console.log('- socket still online -');
            }
            else {
                //// We shouldn't get here
                console.log("Received: '" + message.utf8Data + "'");
            }
        }
    });
});

var settings;
var CONFIG;
function init(s) {
    settings = s;
    CONFIG = settings.CONFIG;
}

function connect() {
    client.connect('wss://eventsub.wss.twitch.tv/ws?keepalive_timeout_seconds=30');
}

module.exports = {
    init,
    connect
};

function subscribe() {
    console.log('Subscribing....');

    ///// This gives us channel redemptions that Twitch provides. e.g. "Highlight my message"
    settings.twitchapi.subscribe({
        'type':'channel.channel_points_automatic_reward_redemption.add',
        'version': '1',
        'condition': {
            'broadcaster_user_id': CONFIG.broadcaster_user_id
        },
        'transport': {
            "method": "websocket",
            "session_id": SESSIONID
        }
    });

    ///// This gives us channel redemptions that are custom. e.g. "Yaht Sea"
    settings.twitchapi.subscribe({
        'type':'channel.channel_points_custom_reward_redemption.add',
        'version': '1',
        'condition': {
            'broadcaster_user_id': CONFIG.broadcaster_user_id
        },
        'transport': {
            "method": "websocket",
            "session_id": SESSIONID
        }
    });

    ///// This gives us bit redemptions.
    settings.twitchapi.subscribe({
        'type':'channel.cheer',
        'version': '1',
        'condition': {
            'broadcaster_user_id': CONFIG.broadcaster_user_id
        },
        'transport': {
            "method": "websocket",
            "session_id": SESSIONID
        }
    });    
}