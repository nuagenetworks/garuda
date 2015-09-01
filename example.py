# -*- coding:utf-8 -*-

import requests
import threading

from time import sleep
from base64 import urlsafe_b64encode


print '---- GET http://localhost:2000/me'
response = requests.get('http://localhost:2000/me', headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST Y3Nwcm9vdDpjc3Byb290'})
print '[%s]\n%s\n' % (response.status_code, response.content)
data = response.json()
encoded_token = urlsafe_b64encode('csproot:%s' % data['api_key'])


def listen_events(token):
    print '---- GET http://localhost:2000/events'
    response = requests.get('http://localhost:2000/events', headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST %s' % encoded_token})
    print '[%s]\n%s\n' % (response.status_code, response.content)


thread = threading.Thread(target=listen_events, name="ListeningPushNotification", kwargs={'token': encoded_token})
thread.start()

print '---- GET http://localhost:2000/enterprises'
response = requests.post('http://localhost:2000/enterprises', headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST %s' % encoded_token}, json={'name': 'Christophe'})
print '[%s]\n%s\n' % (response.status_code, response.content)

print 'Sleeping...'
sleep(10)