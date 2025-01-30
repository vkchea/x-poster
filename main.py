import tweet
import re
import base64
import hashlib
import os

from flask import Flask, request, redirect, session
from authenticator import Authenticator
import authenticator

app = Flask(__name__)
app.secret_key = os.urandom(50)

@app.route("/")
def demo():
    auth = initialize_authenticator()
    twitter = authenticator.oauth2session(auth.client_id, auth.redirect_uri, auth.scopes)
    authorization_url, state = twitter.authorization_url(
        auth.auth_url, code_challenge=auth.code_challenge, code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)

@app.route("/oauth/callback", methods=["GET"])
def callback():
    auth = initialize_authenticator()
    code = request.args.get("code")
    state = session.get("oauth_state")

    twitter = authenticator.oauth2session(auth.client_id, auth.redirect_uri, state)
    token = authenticator.retrieve_token(twitter, auth.token_url, auth.client_secret, auth.code_verifier, code)

    payload = {
        "text": "Learn how to use the user Tweet timeline and user mention timeline endpoints in the X API v2 to explore Tweet https://t.co/56a0vZUx7i"
    }

    response = tweet.post_tweet(payload, token).json()
    return response

"===================================================================================================================="
" Helper Methods "
"===================================================================================================================="
def initialize_authenticator():
    token_url="https://api.x.com/2/oauth2/token"
    client_id=''
    client_secret='-'
    redirect_uri='http://127.0.0.1:5000/oauth/callback'
    scopes = ["tweet.read", "users.read", "tweet.write"]
    auth_url = "https://twitter.com/i/oauth2/authorize"
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8"))
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest()).decode("utf-8").replace("=", "")

    auth = Authenticator(client_id, redirect_uri, scopes, auth_url, code_verifier, code_challenge, token_url, client_secret)
    return auth

if __name__ == "__main__":
    app.run()