import json
import os
import requests


class EditToken:
    token = None
    cookies = None

    def __init__(self):
        self._login()

    def _login(self, filename='mw_api_credentials.json'):
        """
        MediaWiki edits via script require a credentials token. This method fetches that token and returns it.

        :param filename -- The filename where login credentials are stored. Defaults to `mw_api_credentials.json`.
        """
        if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
            print(filename)
            raise IOError('This API requires login credentials. Did you forget to define them?')
        else:
            # Read credentials.
            data = json.load(open(filename))['credentials']
            username = data['username']
            password = data['password']
            headers = {'User-Agent': 'ResMarBot'}
            # First request.
            r1 = requests.post('http://en.wikipedia.org/w/api.php?action=login&format=json',
                               data={'lgname': username, 'lgpassword': password},
                               headers=headers)
            confirmation_token = json.loads(r1.text)['login']['token']
            # Second request.
            r2 = requests.post('http://en.wikipedia.org/w/api.php?action=login&format=json',
                               data={'lgname': username, 'lgpassword': password, 'lgtoken': confirmation_token},
                               headers=headers,
                               cookies=r1.cookies)
            # Save the edit cookies.
            self.cookies = r2.cookies
            # Third (edit token) request.
            params = {'action': 'query', 'prop': 'info', 'titles': 'User:ResMarBot', 'intoken': 'edit'}
            r3 = requests.get("http://en.wikipedia.org/w/api.php", params=params)
            # TODO: Finish this third request.
