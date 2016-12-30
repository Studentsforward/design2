import unittest

class CompatibilityTestCase(unittest.TestCase):

    def test_ssl(self):

        from urllib.request import urlopen

        urlopen('https://askubuntu.com')

    def test_plaid(self):
        from plaid import Client
        import os

        Client.config({
            'url': 'https://tartan.plaid.com',
            'suppress_http_errors': True,
            'suppress_warnings': True
        })

        client = Client(client_id='5824eec946eb126b6a860966',
                        secret=os.environ['SECRET_KEY'])

        client.exchange_token('test,chase,connected')
