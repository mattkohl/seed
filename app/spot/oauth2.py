import base64
import requests
import os
import time


class SpotifyOauthError(Exception):
    pass


def _make_authorization_headers(client_id, client_secret):
    auth_header = base64.b64encode(six.text_type(client_id + ':' + client_secret).encode('ascii'))
    return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}


def is_token_expired(token_info):
    now = int(time.time())
    return token_info['expires_at'] - now < 60


class SpotifyClientCredentials(object):
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id=None, client_secret=None, proxies=None):
        """
        You can either provid a client_id and client_secret to the
        constructor or set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET
        environment variables
        """
        if not client_id:
            client_id = os.getenv('SPOTIFY_CLIENT_ID')

        if not client_secret:
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        if not client_id:
            raise SpotifyOauthError('No client id')

        if not client_secret:
            raise SpotifyOauthError('No client secret')

        self.client_id = client_id
        self.client_secret = client_secret
        self.token_info = None
        self.proxies = proxies

    def get_access_token(self):
        """
        If a valid access token is in memory, returns it
        Else feches a new token and returns it
        """
        if self.token_info and not self.is_token_expired(self.token_info):
            return self.token_info['access_token']

        token_info = self._request_access_token()
        token_info = self._add_custom_values_to_token_info(token_info)
        self.token_info = token_info
        return self.token_info['access_token']

    def _request_access_token(self):
        """Gets client credentials access token """
        payload = { 'grant_type': 'client_credentials'}

        headers = _make_authorization_headers(self.client_id, self.client_secret)

        response = requests.post(self.OAUTH_TOKEN_URL, data=payload,
            headers=headers, verify=True, proxies=self.proxies)
        if response.status_code != 200:
            raise SpotifyOauthError(response.reason)
        token_info = response.json()
        return token_info

    def is_token_expired(self, token_info):
        return is_token_expired(token_info)

    def _add_custom_values_to_token_info(self, token_info):
        """
        Store some values that aren't directly provided by a Web API
        response.
        """
        token_info['expires_at'] = int(time.time()) + token_info['expires_in']
        return token_info


