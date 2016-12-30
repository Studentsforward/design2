from plaid import Client
import os
import pprint

# For testing purposes
Client.config({
    'url': 'https://tartan.plaid.com'
})

client = Client(client_id='5824eec946eb126b6a860966',
                secret=os.environ['SECRET_KEY'])

#response = client.exchange_token('test,chase,connected')

client.auth('chase', {'username': 'plaid_test', 'password': 'plaid_good'})

pprint.pprint(client.balance().json())

pprint.pprint(client.connect_get().json())
