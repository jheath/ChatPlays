# ChatPlays

## Pre-requisites

- Node `https://www.youtube.com/watch?v=J8ZPZq_34aY&t=203s`
- Python `https://youtu.be/m9I-YpOjXVQ?t=149`

## How to get started

1. Clone this repo or download the zip. If you download the zip, navigate to `https://github.com/jheath/ChatPlays` and click the green `Code` button, then `Download ZIP
2. `npm install` to install all the dependencies.
3. Go to https://dev.twitch.tv/console and create an app if you don't have one already. Select `Applications` from the menu and then `Register Your Application`. Fill in the details and click `Create`.
    - Name - Name of your app
    - OAuth Redirect URLs - You can use `http://localhost:3000/auth/twitch/callback`.
    - Category - Select a category that best describes your app.
    - Client Type - Confidential is good.
4. After application is created, you can select the `Manage` button to view the `Client ID` and `Client Secret`. You will need these details in the next step. Also, don't share these details with anyone.
5. Navigate to your project files and copy `config.json.example` to `config.json`.
6. Open config.json and fill in your `client_id`.
7. `node ./index.js`
8. Profit!

## How to get an access token

1. Navigate to `http://localhost:3000` in your favorite browser (assuming application is running).
2. You will be redirected to the Twitch login page. Login with the account you want to monitor.
3. After logging in, you will be redirected back to the application. If everything went well, you will see a message saying `Authentication successful! You can now close this window.`.
4. An access token will be loaded into the application.

### Manually retrieving an access token
This section is not needed if you have followed the steps above, but here for testing purposes.
Add your `client_id` to the following URL, then send it to the user whose stream you want to monitor (e.g. PearGamer7857)
```
https://id.twitch.tv/oauth2/authorize?response_type=token+id_token&client_id=<YOUR CLIENT ID>&redirect_uri=http://localhost:3000&scope=channel:read:redemptions+bits:read+openid+user:read:email&claims={"id_token":{"email":null,"email_verified":null}}&state=c3ab8aa609ea11e793ae92361f002671&nonce=c3ab8aa609ea11e793ae92361f002671
```

When they visit that URL and authorize your app, they will be redirected to a invalid page, but the URL will contain an `access_token` that they need to return to you e.g.
```
http://localhost:3000/
    #access_token=73gl5dipwta5fsfma3ia05woyffbp
    &id_token=eyJhbGciOiJSUzI1NiIsInR5cC6IkpXVCIsImtpZCI6IjEifQ...
    &scope=channel%253Amanage%253Apolls+channel%253Aread%253Apolls+openid
    &state=c3ab8aa609ea11e793ae92361f002671
    &token_type=bearer
```

## Using the application
1. After running `node ./index.js`, you will notice that a YahtSea pygame application will start. This is what displays the current game details and can be captured from OBS.
2. The application responds to chat command, but you can also run commands (coming soon).

## Things to note
### Managing the leaderboard.
1. The leaderboard is managed by the application automatically. The daily leaderboard is reset every day.
2. The history.json file contains the leaderboard history and details about the user's games played.
    - The history.json is backed up every day to the `/backups` folder.

### Redeeming rewards
1. Many users can redeem a reward to play a game of YahtSea at the same time. However, only one game is displayed at a time. The active game user is the only user that can play as well.
