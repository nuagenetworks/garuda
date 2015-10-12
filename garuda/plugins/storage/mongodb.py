# -*- coding: utf-8 -*-
from bambou import NURESTModelController
import pymongo
from bson import ObjectId

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
            self.db[model[0].rest_name].create_index([('_id', pymongo.DESCENDING)], unique=True)

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
        data = self.db[resource_name].find_one({'_id': ObjectId(identifier)})

        if not data:
            return None

        obj = self.instantiate(resource_name)
        obj.from_dict(self._convert_from_dbid(data))

        return obj

    def get_all(self, parent, resource_name, page=None, page_size=None, filter=None, order_by=None):
        """
        """
        ret = []
        data = []
        skip = 0
        total_count = 0

        if not page or not page_size: page = page_size = 0
        elif page > 0: skip = (page - 1) * page_size

        if filter: filter = self._parse_filter(filter)

        if parent:
            if parent.fetcher_for_rest_name(resource_name).relationship == "child":
                data = self.db[resource_name].find({'parentID': parent.id})
            else:
                association_key = '_rel_%s' % resource_name
                association_data = self.db[parent.rest_name].find_one({'_id': ObjectId(parent.id)}, {association_key: 1})

                if not association_key in association_data: return []

                identifiers = [ObjectId(identifier) for identifier in association_data[association_key]]

                data = self.db[resource_name].find({'_id': {'$in': identifiers}}).skip(skip).limit(page_size)
                total_count = self.db[resource_name].find({'_id': {'$in': identifiers}}).count()
        else:
            data = self.db[resource_name].find(filter).skip(skip).limit(page_size)
            total_count = self.db[resource_name].find().count()

        for d in data:
            obj = self.instantiate(resource_name)
            obj.from_dict(self._convert_from_dbid(d))
            ret.append(obj)

        return ret, total_count

    def create(self, resource, parent=None):
        """
        """
        resource.last_updated_date = "now"
        resource.last_updated_by = "me"
        resource.owner = "me"
        resource.parent_type = parent.rest_name if parent else None
        resource.parent_id = parent.id  if parent else None
        resource.id = str(ObjectId())

        validation = self._validate(resource)
        if validation: return validation

        self.db[resource.rest_name].insert_one(self._convert_to_dbid(resource.to_dict()))

        if parent:
            data = self.db[parent.rest_name].find_one({'_id': ObjectId(parent.id)})
            children_key = '_%s' % resource.rest_name
            children = data[children_key] if children_key in data else []
            children.append(resource.id)

            self.db[parent.rest_name].update({'_id': {'$eq': ObjectId(parent.id)}}, {'$set': {children_key: children}})

    def update(self, resource):
        """
        """

        resource.last_updated_date = "now"
        resource.last_updated_by = "me"

        validation = self._validate(resource)
        if validation: return validation

        validation = self._check_equals(resource)
        if validation: return validation

        self.db[resource.rest_name].update({'_id': {'$eq': ObjectId(resource.id)}}, {'$set': self._convert_to_dbid(resource.to_dict())})

    def delete(self, resource, cascade=True):
        """
        """
        if resource.parent_id and resource.parent_type:
            children_key = '_%s' % resource.rest_name
            data = self.db[resource.parent_type].find_one({'_id': ObjectId(resource.parent_id)}, {children_key: 1})
            if data:
                data[children_key].remove(resource.id)
                self.db[resource.parent_type].update({'_id': {'$eq': ObjectId(resource.parent_id)}}, {'$set': data})

        self.delete_multiple(resources=[resource], cascade=cascade)

    def delete_multiple(self, resources, cascade=True):
        """
        """

        for resource in resources:

            if cascade:

                data = self.db[resource.rest_name].find_one({'_id': ObjectId(resource.id)}) # this could be optimized by only getting the children keys

                for children_rest_name in resource.children_rest_names:

                    children_key = '_%s' % children_rest_name

                    if not children_key in data:
                        continue

                    klass = NURESTModelController.get_first_model(children_rest_name)
                    child_resources = [klass(id=identifier) for identifier in data[children_key]]

                    # recursively delete children
                    self.delete_multiple(child_resources)

        self.db[resource.rest_name].remove({'_id': {'$in': [ObjectId(resource.id) for resource in resources]}})



    def assign(self, resource_name, resources, parent):
        """
        """
        self.db[parent.rest_name].update({'_id': {'$eq': ObjectId(parent.id)}}, {'$set': {'_rel_%s' % resource_name: [r.id for r in resources]}})

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

    def _convert_to_dbid(self, data):
        """
        """
        if data and data['ID']:
            data['_id'] = ObjectId(data['ID'])
            del data['ID']

        return data

    def _convert_from_dbid(self, data):
        """
        """
        if data:
            data['ID'] = str(data['_id'])
            del data['_id']

        return data

    def _parse_filter(self, filter):
        """
        """
        # @TODO: this is a very stupid predicate parsing implementation

        components = filter.split(' ')
        attribute = components[0]
        operator = components[1].lower()
        value = components[2]

        if operator == 'contains': operator = '$text'
        elif operator == 'equals': operator = '$eq'
        elif operator == 'in': operator = '$in'
        elif operator == 'not in': operator = '$nin'
        elif operator == '==': operator = '$eq'
        elif operator == '!=': operator = '$neq'
        elif operator == '>': operator = '$gt'
        elif operator == '>=': operator = '$gte'
        elif operator == '<': operator = '$lt'
        elif operator == '<=': operator = '$lte'


        return {attribute: {operator: value}}



