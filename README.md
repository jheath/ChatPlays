## How to get started

1. Clone this repo
2. `npm install` to install all the dependencies.
3. Go to https://dev.twitch.tv/console and create an app. 

4. Copy `config.json.example` to `config.json` and fill in your `client_id`.

5. Add your `client_id` to the following URL, then send it to the user whose stream you want to monitor (e.g. PearGamer7857)
```
https://id.twitch.tv/oauth2/authorize?response_type=token+id_token&client_id=<YOUR CLIENT ID>&redirect_uri=http://localhost:3000&scope=channel:read:redemptions+bits:read+openid+user:read:email&claims={"id_token":{"email":null,"email_verified":null}}&state=c3ab8aa609ea11e793ae92361f002671&nonce=c3ab8aa609ea11e793ae92361f002671
```

6. When they visit that URL and authorize your app, they will be redirected to a invalid page, but the URL will contain an `access_token` that they need to return to you e.g.
```
http://localhost:3000/
    #access_token=73gl5dipwta5fsfma3ia05woyffbp
    &id_token=eyJhbGciOiJSUzI1NiIsInR5cC6IkpXVCIsImtpZCI6IjEifQ...
    &scope=channel%253Amanage%253Apolls+channel%253Aread%253Apolls+openid
    &state=c3ab8aa609ea11e793ae92361f002671
    &token_type=bearer
```

7. Put the token received into the `token` field of `config.json`

8. `node ./index.js`

9. Profit!

