# Author: Liren Huang

import base64, json, requests
from pathlib import Path

AUTH_URL = 'https://api.twitter.com/oauth2/token'
SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json'

def get_access_token():
    """
    Return the access token from Twitter (saved in "keys" file).
    """
    with open('keys', 'r') as f:
        obj = json.load(f)
    if 'ACCESS_TOKEN' in obj:
        return obj['ACCESS_TOKEN']
    CONSUMER_KEY, CONSUMER_SECRET = obj['CONSUMER_KEY'].encode(), obj['CONSUMER_SECRET'].encode()
    base64_token = base64.b64encode(CONSUMER_KEY + b':' + CONSUMER_SECRET)
    data = {'grant_type': 'client_credentials'}
    headers = {'Authorization': b'Basic ' + base64_token, 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    r = requests.post(AUTH_URL, data=data, headers=headers)
    if r.json()['token_type'] != 'bearer':
        raise RuntimeError('the token type is not bearer!')
    token = r.json()['access_token']
    obj["ACCESS_TOKEN"] = token
    with open('keys', 'w') as f:
        json.dump(obj, f)
    return token

def search(params):
    """
    Search using the given parameter dictionary, save the result in a json file and return its path.
    """
    headers = {'Authorization': b'Bearer ' + get_access_token().encode()}
    r = requests.get(SEARCH_URL, params=params, headers=headers)
    return r.json()

def search_url(url):
    """
    Search using a pre-constructed url.
    """
    headers = {'Authorization': b'Bearer ' + get_access_token().encode()}
    r = requests.get(url, headers=headers)
    return r.json()

def save_file(obj, term, parent, option):
    """
    Create a folder for the search term if it doen't already exist. Then save the json object to the file and return its path.
    """
    p = Path(parent)
    if p.exists() and p.is_dir():
        pass
    else:
        p.mkdir()
    p2 = Path(parent, term)
    if p2.exists() and p2.is_dir():
        pass
    else:
        p2.mkdir()
    path = parent + '/' + term + '/' + option + '.json'
    with open(path, 'w') as f:
        json.dump(obj, f)
    return path
