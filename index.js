const express = require('express');
const axios = require('axios');
const tmi = require('tmi.js');
const _ = require('lodash');
const CONFIG = require('./config.json');

const twitchapi = require('./twitchapi.js');
const eventSocket = require('./eventSocket.js');
const yahtSeaChat = require('./src/yahtSeaChat.js');

const { execFile } = require("child_process");

const app = express();

//// Set up the Twitch Chat Connect
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
function main(token) {
    //// Set up the Twitch API
    twitchapi.init(
        {
            CONFIG,
            token
        }
    );

    //// Set up the Twitch Event Web Socket
    eventSocket.init(
        {
            CONFIG,
            twitchapi,
            onBitsRedemption,
            onChannelPointsRedeption
        }
    );

    //// Set up the YahtSea Chat
    yahtSeaChat.init(
        {
            twitchapi
        }
    );

    execFile('python', ['yahtsea_pygame.py'], (error, stdout, stderr) => {
        //nothing to do here
    });

    yahtSeaChat.processCommand();

    eventSocket.connect();
    chatConnect();
}


//// 
function onBitsRedemption(data) {

}

////
function onChannelPointsRedeption(data) {
    //YahtSea reward ID
    if (data.payload.event.reward?.id === CONFIG.yahtseaRewardId) {
        if (data.payload.event['user_name']) {
            yahtSeaChat.processChat('play', data.payload.event['user_name']);
        }
    }
}

function onChatMessage(message, tags) {
    //tags['display-name'] //Display Name
    //tags['username'] //username

    yahtSeaChat.processChat(message, tags['display-name']);
}

// Redirect the user to Twitch for authentication
app.get('/', (req, res) => {
    const twitchAuthUrl = `https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=${CONFIG.client_id}&redirect_uri=http://localhost:3000/auth/twitch/callback&scope=channel:read:redemptions+bits:read+openid+user:read:email+user:write:chat&claims={"id_token":{"email":null,"email_verified":null}}`;
    res.redirect(twitchAuthUrl);
});

// Handle the callback from Twitch
app.get('/auth/twitch/callback', async (req, res) => {
    const { code } = req.query;

    try {
        const response = await axios.post('https://id.twitch.tv/oauth2/token', null, {
            params: {
                client_id: CONFIG.client_id,
                client_secret: CONFIG.client_secret,
                code,
                grant_type: 'authorization_code',
                redirect_uri: 'http://localhost:3000/auth/twitch/callback',
            },
        });

        const { access_token } = response.data;

        // Store the access token (you can replace this with your own storage mechanism)
        console.log('Access Token:', access_token);

        res.send('Authentication successful! You can now close this window.');

        main(access_token);
    } catch (error) {
        console.error('Error fetching access token:', error);
        res.status(500).send('Authentication failed.');
    }
});

app.listen(3000, () => {
    console.log(`Server is running. Authenticate on Twitch: http://localhost:3000`);
});
