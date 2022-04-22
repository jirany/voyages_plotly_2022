import os

voyages_auth_token=os.environ['voyages_auth_token']

headers={'Authorization': 'Token %s' %voyages_auth_token}

base_url="http://127.0.0.1:8000/"