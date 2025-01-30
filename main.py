import tweet
import re
import base64
import hashlib
import os

from flask import Flask, request, redirect, session
from authenticator import Authenticator

app = Flask(__name__)
app.secret_key = os.urandom(50)

@app.route("/")
def demo():
    auth = initialize_authenticator()
    session["oauth_state"] = auth.authorization_url()
    return redirect(auth.twitter.redirect_uri)

@app.route("/oauth/callback", methods=["GET"])
def callback():
    state = session.get("oauth_state")
    code = request.args.get("code")
    print(state)

    # token = retrieve_token(twitter, token_url, client_secret, code_verifier, code)
    # print("token: ", token)
    # payload = {
    #     "text": "Learn how to use the user Tweet timeline and user mention timeline endpoints in the X API v2 to explore Tweet https://t.co/56a0vZUx7i"
    # }
    # response = tweet.post_tweet(payload, token).json()
    # return response

"===================================================================================================================="
" Helper Methods "
"===================================================================================================================="
def initialize_authenticator():
    client_id=''
    redirect_uri='http://127.0.0.1:5000/oauth/callback'
    scopes = ["tweet.read", "users.read", "tweet.write"]
    auth_url = "https://twitter.com/i/oauth2/authorize"
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8"))
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest()).decode("utf-8").replace("=", "")

    auth = Authenticator(client_id, redirect_uri, scopes, auth_url, code_challenge)
    return auth

if __name__ == "__main__":
    app.run()