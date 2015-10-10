# -*- coding: utf-8 -*-
from uuid import uuid4
from bambou import NURESTModelController
from pymongo import MongoClient

from garuda.core.plugins import GAModelControllerPlugin, GAPluginManifest
from garuda.core.models import GAError
from garuda.core.lib import SDKsManager


class GAMongoSotragePlugin(GAModelControllerPlugin):
    """
    """

    def __init__(self, db_name='garuda', mongo_uri='mongodb://127.0.0.1:27017'):
        """
        """
        super(GAMongoSotragePlugin, self).__init__()

        self.mongo = MongoClient(mongo_uri)
        self.db = self.mongo[db_name]
        self.sdk = None

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='Garuda MongoDB Storage Plugin', version=1.0, identifier="garuda.plugins.storage.mongodb")

    def did_register(self):
        """
        """
        self.sdk = SDKsManager().get_sdk("current")

        root_rest_name = self.sdk.SDKInfo.root_object_class().rest_name

        # insert the default user
        if not self.db['root_rest_name'].count():
            self.db[root_rest_name].insert({'ID': '1', 'userName': 'root', 'password': 'password'})

    def should_manage(self, resource_name, identifier):
        """
        """
        return True

    def instantiate(self, resource_name):
        """
        """
        klass = NURESTModelController.get_first_model(resource_name)
        return klass()

    def get(self, resource_name, identifier):
        """
        """
        data = self.db[resource_name].find_one({'ID': identifier})

        if not data: return None

        obj = self.instantiate(resource_name)
        obj.from_dict(data)
        return obj

    def get_all(self, parent, resource_name):
        """
        """
        ret = []

        if parent:
            data = self.db[resource_name].find({'parentID': parent.id})
        else:
            data = self.db[resource_name].find()


        for d in data:
            obj = self.instantiate(resource_name)
            obj.from_dict(d)
            ret.append(obj)

        return ret

    def create(self, resource, parent=None):
        """
        """
        resource.last_updated_date = "now"
        resource.last_updated_by = "me"
        resource.owner = "me"
        resource.parent_type = parent.rest_name if parent else None
        resource.parent_id = parent.id  if parent else None
        resource.id = str(uuid4())

        validation = self._validate(resource)
        if validation: return validation

        self.db[resource.rest_name].insert(resource.to_dict())

    def update(self, resource):
        """
        """

        resource.last_updated_date = "now"
        resource.last_updated_by = "me"

        validation = self._validate(resource)
        if validation: return validation

        validation = self._check_equals(resource)
        if validation: return validation

        self.db[resource.rest_name].update({'ID': {'$eq': resource.id}}, {'$set': resource.to_dict()})


    def delete(self, resource):
        """
        """
        self.db[resource.rest_name].remove({'ID': resource.id})


    def assign(self, resource_name, resources, parent):
        """
        """
        print "ASSIGNED objects %s of type %s to parent %s %s" % (resources, resource_name, parent.rest_name, parent.id)

    def _validate(self, resource):
        """
        """
        if resource.validate():
            return None

        errors = []
        for property_name, error in resource.errors.iteritems():
            errors.append(GAError(type=GAError.TYPE_CONFLICT, title=error["title"], description=error["description"], property_name=error['remote_name']))
        return errors


    def _check_equals(self, resource):
        """
        """
        stored_obj = self.get(resource.rest_name, resource.id)
        if not stored_obj.rest_equals(resource): return None

        return GAError(type=GAError.TYPE_CONFLICT, title="No changes to modify the entity", description="There are no attribute changes to modify the entity.")