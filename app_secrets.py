import os

voyages_auth_token=os.environ['voyages_auth_token']

headers={'Authorization': 'Token %s' %voyages_auth_token}
base_url="https://voyages3-api.crc.rice.edu/"
