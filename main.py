import base64
import hashlib
import os
import re
import requests

from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, render_template

app = Flask(__name__)
app.secret_key = os.urandom(50)

client_id=''
client_secret=''
redirect_uri='http://127.0.0.1:5000/oauth/callback'

auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.x.com/2/oauth2/token"

scopes = ["tweet.read", "users.read", "tweet.write"]

code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

API_KEY=''
API_SECRET=''
ACCESS_TOKEN=''
ACCESS_TOKEN_SECRET=''

def post_tweet(payload, new_token):
    print("Tweeting!")
    return requests.request(
        "POST",
        "https://api.x.com/2/tweets",
        json=payload,
        headers={
            "Authorization": "Bearer {}".format(new_token["access_token"]),
            "Content-Type": "application/json",
        },
    )

@app.route("/")
def demo():
    global twitter
    twitter = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)
    authorization_url, state = twitter.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)

@app.route("/oauth/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    print(request)
    token = twitter.fetch_token(
        token_url=token_url,
        client_secret=client_secret,
        code_verifier=code_verifier,
        code=code,
    )
    print("token: ", token)
    payload = {
        "text": "Learn how to use the user Tweet timeline and user mention timeline endpoints in the X API v2 to explore Tweet https://t.co/56a0vZUx7i"
    }
    response = post_tweet(payload, token).json()
    return response


if __name__ == "__main__":
    app.run()