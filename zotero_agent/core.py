"""Read-only access to the local Zotero library."""

import re
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests


ZOTERO_URL = 'http://127.0.0.1:23119/api'


class Zotero:
    def __init__(self):
        self.session = requests.Session()
        self.session.trust_env = False
        response = self._get('/', timeout=20)
        self.session.headers['Zotero-Server-ID'] = response.headers['Zotero-Server-ID']

    def _get(self, path, timeout=30):
        response = self.session.get(ZOTERO_URL + path, timeout=timeout)
        response.raise_for_status()
        return response

    def items(self):
        return self._get('/users/0/items/top?format=json').json()

    def children(self, key):
        return self._get(f'/users/0/items/{key}/children').json()

    def pdf(self, attachment):
        response = self._get('/users/0/items/' + attachment['key'] + '/file/view/url')
        parsed = urlparse(response.text.strip())
        if parsed.scheme != 'file':
            raise ValueError('附件尚未下载到本机')
        path = unquote(parsed.path)
        if re.match(r'^/[A-Za-z]:', path):
            path = path[1:]
        result = Path(path)
        if not result.is_file():
            raise FileNotFoundError(result)
        return result
