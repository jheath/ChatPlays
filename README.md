# ChatPlays

## Pre-requisites

- Node `https://www.youtube.com/watch?v=J8ZPZq_34aY&t=203s`
- Python `https://youtu.be/m9I-YpOjXVQ?t=149`

## How to Get Started

1. Clone this repo or download the zip. If you download the zip, navigate to `https://github.com/jheath/ChatPlays` and click the green `Code` button, then `Download ZIP`.
2. Extract the files to a location of your choice, then run `npm install` in the terminal at the root of the project.
3. Go to https://dev.twitch.tv/console and create an app if you don't have one already. Select `Applications` from the menu and then `Register Your Application`. Fill in the details and click `Create`.
   - **Name**: Name of your app
   - **OAuth Redirect URLs**: Provide `http://localhost:3000/auth/twitch/callback`. Also, if using Postman to test calls, add `https://oauth.pstmn.io/v1/callback` as well.
   - **Category**: Select a category that best describes your app.
   - **Client Type**: Confidential is good.
4. After the application is created, you can select the `Manage` button to view the `Client ID` and `Client Secret`. You will need these details in the next step. Do not share these details with anyone.
5. Navigate to your project files and copy `config.json.example` to `config.json`.
6. Open `config.json` and fill in your `client_id`, `client_secret`, and `yahtSeaRewardId`.
7. Run `node ./index.js` to start application.
8. Profit!

## How to Authenticate

1. Open your favorite browser and go to `http://localhost:3000` after running `node ./index.js`.
2. You will be redirected to the Twitch login page. Log in with the account you wish to monitor.
3. Upon logging in, you will be redirected back to the application. If the process was successful, you will see a message saying, `Authentication successful! You can now close this window.`

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
1. After running `node ./index.js`, you will notice that a YahtSea pygame application will open. This is what displays the current game details and can be captured from OBS.
2. The application responds to chat command to play a game of Yahtsea:
    - `roll` - This command will roll the dice for the user.
    - `hold [1-6]` - This command will hold the dice for the user. The dice parameter is a comma-separated list of dice to hold (e.g. `hold 1,2,3`).
    - `resume` - The GUI timeout the user if the game takes longer than 3 minutes. This command will resume the users game assuming it is not in usedd by another user.
    - `end_round` - This command will hold all dice and end the round scoring the points.
3. You can also run commands from terminal:
    - `help` - This command will display the available commands.
    - [coming soon]

## Things to note
### Managing the leaderboard.
1. The leaderboard is managed by the application automatically. The daily leaderboard is reset every day.
2. The history.json file ***stores game data and should not be deleted***. It contains the leaderboard history and details for all users.
    - The history.json is backed up every day to the `/backups` folder.

### Redeeming rewards
1. Users can redeem a reward to play a game of YahtSea at the same time. However, only one game is displayed at a time. The active game user is the only user that can run the following commands:
   - `roll`
   - `hold [1-6]`
   - `resume`
   - `end_round`
2. All users can run the following commands at any given time:
   - `leaderboard`
