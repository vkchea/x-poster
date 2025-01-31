import re
import base64
import hashlib
import os

token_url="https://api.x.com/2/oauth2/token"
client_id=''
client_secret=''
redirect_uri='http://127.0.0.1:5000/oauth/callback'
scopes = ["tweet.read", "users.read", "tweet.write"]
auth_url = "https://twitter.com/i/oauth2/authorize"
code_verifier = re.sub("[^a-zA-Z0-9]+", "", base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8"))
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest()).decode("utf-8").replace("=", "")



