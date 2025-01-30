
from requests_oauthlib import OAuth2Session


def retrieve_token(twitter, token_url, client_secret, code_verifier, code):
    return twitter.fetch_token(token_url=token_url,
                               client_secret=client_secret,
                               code_verifier=code_verifier,
                               code=code)


class Authenticator:

    def __init__(self, client_id, redirect_uri, scopes, auth_url, code_challenge):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.auth_url = auth_url
        self.code_challenge = code_challenge
        self.twitter = self.oauth2session()  # Call instance method properly

    def oauth2session(self):
        return OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scopes)

    def authorization_url(self):
        return self.twitter.authorization_url(
            self.auth_url, code_challenge=self.code_challenge, code_challenge_method="S256"
        )

