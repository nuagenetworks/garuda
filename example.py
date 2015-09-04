# -*- coding:utf-8 -*-

import requests
import threading

from time import sleep
from base64 import urlsafe_b64encode

base_url = 'http://localhost:2000/nuage/api/v3_2'


print '---- GET %s/me' % base_url
response = requests.get('%s/me' % base_url, headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST Y3Nwcm9vdDpjc3Byb290'})
print '[%s]\n%s\n' % (response.status_code, response.content)
data = response.json()
encoded_token = urlsafe_b64encode('csproot:%s' % data['APIKey'])

print '---- GET %s/enterprises' % base_url
response = requests.get('%s/enterprises' % base_url, headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST %s' % encoded_token})
print '[%s]\n%s\n' % (response.status_code, response.content)


# def listen_events(token):
#     print '---- GET %s/events' % base_url
#     response = requests.get('%s/events' % base_url, headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST %s' % encoded_token})
#     print '[%s]\n%s\n' % (response.status_code, response.content)
#
#
# thread = threading.Thread(target=listen_events, name="ListeningPushNotification", kwargs={'token': encoded_token})
# thread.start()

print '---- POST %s/enterprises' % base_url
response = requests.post('%s/enterprises' % base_url, headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST %s' % encoded_token}, json={'name': 'Christophe'})
print '[%s]\n%s\n' % (response.status_code, response.content)

data = response.json()
enterprise_id = data['ID']

print 'Waiting...\n\n'
sleep(8)

print '---- DELETE %s/enterprises/%s' % (base_url, enterprise_id)
response = requests.delete('%s/enterprises/%s' % (base_url, enterprise_id), headers={'X-Nuage-Organization': 'csp', 'Authorization': 'XREST %s' % encoded_token}, json={'name': 'Christophe'})
print '[%s]\n%s\n' % (response.status_code, response.content)