# -*- coding: utf-8 -*-

from vsdhelpers import VSDKFactory

from bambou import NURESTModelController
from bambou.nurest_session import _NURESTSessionCurrentContext
from garuda.config import GAConfig


class ModelsController(object):
    """

    """
    def __init__(self):
        """
        """
        self._vsdk = VSDKFactory.get_vsdk_package()
        self._vsd_session = self._vsdk.NUVSDSession(username=GAConfig.VSD_USERNAME, password=GAConfig.VSD_PASSWORD, enterprise=GAConfig.VSD_ENTERPRISE, api_url=GAConfig.VSD_API_URL)
        self._vsd_session.start()

    def get_objects(self, parent, resource_name):
        """
        """
        fetcher = parent.fetcher_for_rest_name(resource_name)

        if fetcher is None:
            return None

        return fetcher.get()

    def _use_session(self):
        """
        """
        _NURESTSessionCurrentContext.session = self._vsd_session

    def get_object(self, resource_name, resource_value):
        """
        """
        # json_data = '{"allowGatewayManagement": true, "DHCPLeaseInterval": 24, "floatingIPsQuota": 1000, "enterpriseProfileID": "0e0c8e99-ea27-4c1a-9fdb-40f9a9e2e60d", "parentID": null, "owner": "8a6f0e20-a4db-4878-ad84-9cc61756cd5e", "LDAPEnabled": false, "description": "Default Enterprise", "associatedEnterpriseSecurityID": "6adcb017-37a1-4359-a2a2-311d437bc701", "ID": "b554017b-8f51-4a39-8139-08a3d7f01951", "LDAPAuthorizationEnabled": false, "associatedKeyServerMonitorID": "31d5dd95-fa9d-4644-bc55-f3a6d76bedd8", "lastUpdatedDate": 1439399480000, "floatingIPsUsed": 0, "avatarType": null, "parentType": null, "lastUpdatedBy": "43f8868f-4bc1-472c-9d19-533dcfcb1ee0", "associatedGroupKeyEncryptionProfileID": "2eed9304-15bf-4593-bdd8-417de9a77670", "creationDate": 1439399480000, "allowTrustedForwardingClass": true, "customerID": 10004, "name": "Triple A", "avatarData": null, "receiveMultiCastListID": "e19e38fa-86f8-4119-a4eb-95a38e7dda4f", "allowedForwardingClasses": ["A", "B", "C", "D", "E", "F"], "sendMultiCastListID": "ead49282-7ce7-4ac4-8e65-29e5af2b2331", "allowAdvancedQOSConfiguration": true}';
        #
        # return NUEnterprise(data=json.loads(json_data))

        self._use_session()

        klass = NURESTModelController.get_first_model(resource_name)
        obj = klass(id=resource_value)

        if obj is None:
            return None

        (_, connection) = obj.fetch()

        if connection.response.status_code >= 300:
            return None

        return obj

    def create_object(self, resource_name):
        """
        """
        self._use_session()

        klass = NURESTModelController.get_first_model(resource_name)
        obj = klass()

        # TODO: Uncomment this line once validation is working
        # obj.validate()
        return obj

    def save_object(self, object, parent=None, attributes={}):
        """
        """
        self._use_session()

        object.from_dict(attributes)

        # TODO: Uncomment this line once validation is working
        # object.validate()

        if len(object.errors) > 0:
            return object

        if object.id:

            (object, connection) = object.save()

            if connection.response.status_code >= 300:
                return False  # TODO: This is temporarely bad

            return object

        if parent:
            (object, connection) = parent.create_child(object)

            if connection.response.status_code >= 300:
                return False  # TODO: This is temporarely bad

            return object

        else:
            raise Exception('Save object error')

    def delete_object(self, object):
        """
        """
        self._use_session()

        object.delete()

    def get_current_user(self):
        """
        """
        self._use_session()

        return self._vsd_session.user

    def authenticate_user(self, username, password, enterprise):
        """
        """
        session = self._vsdk.NUVSDSession(username=username, password=password, enterprise=enterprise, api_url=GAConfig.VSD_API_URL)
        session.start()

        return session.user
