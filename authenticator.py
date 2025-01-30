from requests_oauthlib import OAuth2Session

class Authenticator:
    def __init__(self, client_id, redirect_uri, scopes, auth_url, code_verifier, code_challenge, token_url, client_secret):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.auth_url = auth_url
        self.code_challenge = code_challenge
        self.token_url = token_url
        self.client_secret = client_secret
        self.code_verifier = code_verifier

def retrieve_token(twitter, token_url, client_secret, code_verifier, code):
    return twitter.fetch_token(token_url=token_url,
                               client_secret=client_secret,
                               code_verifier=code_verifier,
                               code=code)

def oauth2session(client_id, redirect_uri, scopes):
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)



