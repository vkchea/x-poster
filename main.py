import tweet
import os

from flask import Flask, request, redirect, session
from requests_oauthlib import OAuth2Session
from openai import OpenAI

import authenticator as auth

app = Flask(__name__)
app.secret_key = os.urandom(50)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

@app.route("/")
def demo():
    client = OpenAI(
        api_key=""
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content": "write a haiku about ai"}
        ]
    )

    print(completion.choices[0].message)
    twitter = OAuth2Session(auth.client_id, redirect_uri=auth.redirect_uri, scope=auth.scopes)
    authorization_url, state = twitter.authorization_url(
        auth.auth_url, code_challenge=auth.code_challenge, code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)

@app.route("/oauth/callback", methods=["GET"])
def callback():
    code=request.args.get("code")
    state = session.get("oauth_state")
    oauth_session = OAuth2Session(auth.client_id, redirect_uri=auth.redirect_uri, state=state)

    token = oauth_session.fetch_token(auth.token_url, authorization_response=request.url, client_secret=auth.client_secret, code_verifier=auth.code_verifier, code=code)
    session["oauth_token"] = token

    payload = {
        "text": "Learn how to use the user Tweet timeline and user mention timeline endpoints in the X API v2 to explore Tweet https://t.co/56a0vZUx7i"
    }

    response = tweet.post_tweet(payload, token).json()
    return response

if __name__ == "__main__":
    app.run()