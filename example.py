# -*- coding:utf-8 -*-

import requests
import threading
import json

from pprint import pprint
from time import sleep
from base64 import urlsafe_b64encode

base_url = 'http://localhost:2000/nuage/api/v3_2'


def print_response(response):
    """
    """
    pprint('[%s]' % response.status_code)
    pprint(json.loads(response.content))


print '\n---- GET %s/me' % base_url
response = requests.get('%s/me' % base_url, headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST Y3Nwcm9vdDpjc3Byb290'})
print_response(response)
data = response.json()[0]
encoded_token = urlsafe_b64encode('csproot:%s' % data['APIKey'])

print '\n---- GET %s/enterprises' % base_url
response = requests.get('%s/enterprises' % base_url, headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST %s' % encoded_token})
print_response(response)


def listen_events(token):
    print '---- GET %s/events' % base_url
    response = requests.get('%s/events' % base_url, headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST %s' % encoded_token})
    print_response(response)


thread = threading.Thread(target=listen_events, name="ListeningPushNotification", kwargs={'token': encoded_token})
thread.start()

print '\n---- POST %s/enterprises' % base_url
response = requests.post('%s/enterprises' % base_url, headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST %s' % encoded_token}, json={'name': 'GARUDA'})
print_response(response)

data = response.json()
enterprise_id = data['ID']

print 'Waiting...\n\n'
sleep(8)

print '\n---- DELETE %s/enterprises/%s' % (base_url, enterprise_id)
response = requests.delete('%s/enterprises/%s' % (base_url, enterprise_id), headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST %s' % encoded_token}, json={'name': 'GARUDA'})
print_response(response)