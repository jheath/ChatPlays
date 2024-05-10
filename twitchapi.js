const axios = require('axios');
var _ = require('lodash');

function subscribe(payload) {
    axios.post('https://api.twitch.tv/helix/eventsub/subscriptions', payload,
    {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+CONFIG.token,
            'Client-Id': CONFIG.client_id
        }
    })
    .then(function (response) {
        if (_.get(response, 'data.data.0.status') === 'enabled') {
            console.log(' Subscribed to: %s', _.get(response, 'data.data.0.type'));
        }
        else {
            console.log('%j',response.data);
        }
    })
    .catch(function (error) {
        console.log(error);
    });
}

//// Not needed yet?
function getToken() {
    axios.post('https://id.twitch.tv/oauth2/token',
    {
        client_id: CONFIG.client_id,
        client_secret: CONFIG.client_secret,
        grant_type: 'client_credentials'
    }, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(function (response) {
        console.log('%j',response.data);
    })
    .catch(function (error) {
        console.log(error);
    });
}

var settings;
var CONFIG;
function init(s) {
    settings = s;
    CONFIG = settings.CONFIG;
}

module.exports = {
    init,
    subscribe
};