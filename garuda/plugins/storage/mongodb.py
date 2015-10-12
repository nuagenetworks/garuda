# -*- coding: utf-8 -*-
from uuid import uuid4
from bambou import NURESTModelController
import pymongo

from garuda.core.models import GAError, GAPluginManifest
from garuda.core.plugins import GAStoragePlugin
from garuda.core.lib import SDKLibrary


class GAMongoStoragePlugin(GAStoragePlugin):
    """
    """

    def __init__(self, db_name='garuda', mongo_uri='mongodb://127.0.0.1:27017', db_initialization_function=None):
        """
        """
        super(GAMongoStoragePlugin, self).__init__()

        self.mongo = pymongo.MongoClient(mongo_uri)
        self.db = self.mongo[db_name]
        self.sdk = None

        self.db_initialization_function = db_initialization_function

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='mongodb', version=1.0, identifier="garuda.plugins.storage.mongodb")

    def did_register(self):
        """
        """
        self.sdk = SDKLibrary().get_sdk('default')
        root_rest_name = self.sdk.SDKInfo.root_object_class().rest_name

        for model in NURESTModelController.get_all_models():
            self.db[model[0].rest_name].create_index([('ID', pymongo.DESCENDING)], unique=True)
            self.db[model[0].rest_name].create_index('parentID')

        if self.db_initialization_function:
            self.db_initialization_function(db=self.db, root_rest_name=root_rest_name)

    def should_manage(self, resource_name, identifier):
        """
        """
        return True

    def instantiate(self, resource_name):
        """
        """
        klass = NURESTModelController.get_first_model(resource_name)
        return klass()

    def get(self, resource_name, identifier, filter=None):
        """
        """
        data = self.db[resource_name].find_one({'ID': identifier})

        if not data:
            return None

        obj = self.instantiate(resource_name)
        obj.from_dict(data)

        return obj

    def get_all(self, parent, resource_name, filter=None):
        """
        """
        ret = []
        data = []

        if parent:
            if parent.fetcher_for_rest_name(resource_name).relationship == "child":
                data = self.db[resource_name].find({'parentID': parent.id})
            else:
                association_key = '_rel_%s' % resource_name
                association_data = self.db[parent.rest_name].find_one({'ID': parent.id}, {association_key: 1})

                if not association_key in association_data: return []

                data = self.db[resource_name].find({'ID': {'$in': association_data[association_key]}})
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

        self.db[resource.rest_name].insert_one(resource.to_dict())

        if parent:
            data = self.db[parent.rest_name].find_one({'ID': parent.id})
            children_key = '_%s' % resource.rest_name
            children = data[children_key] if children_key in data else []
            children.append(resource.id)

            self.db[parent.rest_name].update({'ID': {'$eq': parent.id}}, {'$set': {children_key: children}})

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

    def delete(self, resource, cascade=True):
        """
        """
        if resource.parent_id and resource.parent_type:
            children_key = '_%s' % resource.rest_name
            data = self.db[resource.parent_type].find_one({'ID': resource.parent_id}, {children_key: 1})
            if data:
                data[children_key].remove(resource.id)
                self.db[resource.parent_type].update({'ID': {'$eq': resource.parent_id}}, {'$set': data})

        self.delete_multiple(resources=[resource], cascade=cascade)

    def delete_multiple(self, resources, cascade=True):
        """
        """

        for resource in resources:

            if cascade:

                data = self.db[resource.rest_name].find_one({'ID': resource.id}) # this could be optimized by only getting the children keys

                for children_rest_name in resource.children_rest_names:

                    children_key = '_%s' % children_rest_name

                    if not children_key in data:
                        continue

                    klass = NURESTModelController.get_first_model(children_rest_name)
                    child_resources = [klass(id=identifier) for identifier in data[children_key]]

                    # recursively delete children
                    self.delete_multiple(child_resources)

        self.db[resource.rest_name].remove({'ID': {'$in': [resource.id for resource in resources]}})



    def assign(self, resource_name, resources, parent):
        """
        """
        self.db[parent.rest_name].update({'ID': {'$eq': parent.id}}, {'$set': {'_rel_%s' % resource_name: [r.id for r in resources]}})

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
