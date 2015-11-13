# -*- coding: utf-8 -*-
from bambou import NURESTModelController
import pymongo
from datetime import datetime
import calendar
import time
from bson import ObjectId

from garuda.core.models import GAError, GAPluginManifest, GAStoragePluginQueryResponse
from garuda.core.plugins import GAStoragePlugin
from garuda.core.lib import GASDKLibrary

class GAMongoStoragePlugin(GAStoragePlugin):
    """
    """

    def __init__(self, db_name='garuda', mongo_uri='mongodb://127.0.0.1:27017', db_initialization_function=None, sdk_identifier='default'):
        """
        """
        super(GAMongoStoragePlugin, self).__init__()

        self.mongo = pymongo.MongoClient(mongo_uri)
        self.db = self.mongo[db_name]
        self.sdk = None
        self.sdk_identifier = sdk_identifier
        self._permissions_controller = None
        self.db_initialization_function = db_initialization_function

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='mongodb', version=1.0, identifier="garuda.plugins.storage.mongodb")

    @property
    def permissions_controller(self):
        """
        """
        if not self._permissions_controller:
            self._permissions_controller = self.core_controller.permissions_controller

        return self._permissions_controller

    def did_register(self):
        """
        """
        self.sdk = GASDKLibrary().get_sdk(self.sdk_identifier)

        if self.db_initialization_function:
            self.db_initialization_function(db=self.db, root_object_class=self.sdk.SDKInfo.root_object_class())

    def should_manage(self, resource_name, identifier):
        """
        """
        return True

    def instantiate(self, resource_name):
        """
        """
        klass = NURESTModelController.get_first_model_with_rest_name(resource_name)
        return klass()

    def count(self, user_identifier, parent, resource_name, filter=None):
        """
        """
        ret = self._get_children_raw_data(user_identifier=user_identifier, parent=parent, resource_name=resource_name, filter=filter, grand_total=False)
        return GAStoragePluginQueryResponse.init_with_data(data=None, count=ret.count)

    def get(self, user_identifier, resource_name, identifier=None, filter=None):
        """
        """
        if identifier and not ObjectId.is_valid(identifier):
            return GAStoragePluginQueryResponse.init_with_error(error_type=GAError.TYPE_NOTFOUND,
                                                                title='Resource not found',
                                                                description='Could not find resource')

        query_filter = {}
        if filter:
            query_filter = self._parse_filter(filter)

        if identifier:
            data = self.db[resource_name].find_one({'$and': [{'_id': ObjectId(identifier)}, query_filter]})
        else:
            data = self.db[resource_name].find_one(query_filter)

        if not data:
            return GAStoragePluginQueryResponse.init_with_error(error_type=GAError.TYPE_NOTFOUND,
                                                                title='Resource not found',
                                                                description='Could not find resource')

        obj = self.instantiate(resource_name)
        obj.from_dict(self._convert_from_dbid(data))

        if not self.permissions_controller.has_permission(resource=user_identifier, target=obj, permission='read'):
            return GAStoragePluginQueryResponse.init_with_error(error_type=GAError.TYPE_UNAUTHORIZED,
                                                                title='Permission Denied',
                                                                description='You do not have permission to access this object')

        return GAStoragePluginQueryResponse.init_with_data(data=obj)

    def get_all(self, user_identifier, parent, resource_name, page=None, page_size=None, filter=None, order_by=None):
        """
        """
        objects = []

        # TODO: this is for the demo :)
        order_by = [('type', pymongo.ASCENDING), ('name', pymongo.ASCENDING), ('title', pymongo.ASCENDING), ('creationDate', pymongo.ASCENDING)]

        response = self._get_children_raw_data(user_identifier=user_identifier, parent=parent, resource_name=resource_name, page=page, page_size=page_size, filter=filter, order_by=order_by, grand_total=True)

        if response.data:
            for d in response.data:
                obj = self.instantiate(resource_name)
                obj.from_dict(self._convert_from_dbid(d))
                objects.append(obj)

        return GAStoragePluginQueryResponse.init_with_data(data=objects, count=response.count)

    def create(self, user_identifier, resource, parent=None):
        """
        """
        # if parent and not self.permissions_controller.has_permission(resource=user_identifier, target=parent, permission='write'):
        #     return GAStoragePluginQueryResponse.init_with_error(error_type=GAError.TYPE_UNAUTHORIZED,
        #                                                         title='Permission Denied',
        #                                                         description='You do not have permission to create this object')

        resource.creation_date = time.time()
        resource.last_updated_date = resource.creation_date
        resource.owner = resource.owner if resource.owner else user_identifier
        resource.parent_type = parent.rest_name if parent else None
        resource.parent_id = parent.id if parent else None
        resource.id = str(ObjectId())

        validation_errors = self._validate(resource)
        if validation_errors:
            return GAStoragePluginQueryResponse.init_with_errors(errors=validation_errors)

        self.db[resource.rest_name].insert_one(self._convert_to_dbid(resource.to_dict()))

        self.permissions_controller.create_permission(resource=user_identifier, target=resource, permission='all')

        if parent:
            data = self.db[parent.rest_name].find_one({'_id': ObjectId(parent.id)})
            children_key = '_%s' % resource.rest_name
            children = data[children_key] if children_key in data else []
            children.append(resource.id)

            self.db[parent.rest_name].update({'_id': {'$eq': ObjectId(parent.id)}}, {'$set': {children_key: children}})

        return GAStoragePluginQueryResponse.init_with_data(data=resource)

    def update(self, user_identifier, resource):
        """
        """
        if not self.permissions_controller.has_permission(resource=user_identifier, target=resource, permission='write'):
            return GAStoragePluginQueryResponse.init_with_error(error_type=GAError.TYPE_UNAUTHORIZED,
                                                                title='Permission Denied',
                                                                description='You do not have permission to update this object')

        resource.last_updated_date = time.time()

        validation_errors = self._validate(resource)
        if validation_errors:
            return GAStoragePluginQueryResponse.init_with_errors(errors=validation_errors)

        self.db[resource.rest_name].update({'_id': {'$eq': ObjectId(resource.id)}}, {'$set': self._convert_to_dbid(resource.to_dict())})

        return GAStoragePluginQueryResponse.init_with_data(data=resource)

    def delete(self, user_identifier, resource, cascade=True):
        """
        """

        if not self.permissions_controller.has_permission(resource=user_identifier, target=resource, permission='write'):
            return GAStoragePluginQueryResponse.init_with_error(error_type=GAError.TYPE_UNAUTHORIZED,
                                                                title='Permission Denied',
                                                                description='You do not have permission to delete this object')

        if resource.parent_id and resource.parent_type:
            children_key = '_%s' % resource.rest_name
            data = self.db[resource.parent_type].find_one({'_id': ObjectId(resource.parent_id)}, {children_key: 1})
            if data:
                data[children_key].remove(resource.id)
                self.db[resource.parent_type].update({'_id': {'$eq': ObjectId(resource.parent_id)}}, {'$set': data})

        self.delete_multiple(user_identifier=user_identifier, resources=[resource], cascade=cascade)

        return GAStoragePluginQueryResponse(data=resource)

    def delete_multiple(self, user_identifier, resources, cascade=True):
        """
        """
        for resource in resources:

            if cascade:

                data = self.db[resource.rest_name].find_one({'_id': ObjectId(resource.id)})  # this could be optimized by only getting the children keys

                if not data:
                    return

                for children_rest_name in resource.children_rest_names:

                    children_key = '_%s' % children_rest_name

                    if children_key not in data or not len(data[children_key]):  # pragma: no cover
                        # there is a feature with the python optimizer that makes coverage unable to mark this as covered
                        # I tried manually, its fine
                        continue

                    klass = NURESTModelController.get_first_model_with_rest_name(children_rest_name)
                    child_resources = [klass(id=identifier) for identifier in data[children_key]]

                    # recursively delete children
                    self.delete_multiple(user_identifier=user_identifier, resources=child_resources, cascade=True)

        self.db[resources[0].rest_name].remove({'_id': {'$in': [ObjectId(resource.id) for resource in resources]}})
        self.permissions_controller.remove_all_permissions_for_target(target=resource)

    def assign(self, user_identifier, resource_name, resources, parent):
        """
        """
        self.db[parent.rest_name].update({'_id': {'$eq': ObjectId(parent.id)}}, {'$set': {'_rel_%s' % resource_name: [r.id for r in resources]}})

    # UTILITIES

    def _get_children_raw_data(self, user_identifier, parent, resource_name, page=None, page_size=None, filter=None, order_by=None, grand_total=True):
        """
        """
        skip = 0
        total_count = 0
        query_filter = {}
        data = None

        page = int(page) if page else 0
        page_size = int(page_size) if page_size else 0

        if page > 0:
            skip = page * page_size

        if filter:
            query_filter = self._parse_filter(filter)

        if parent and parent.fetcher_for_rest_name(resource_name).relationship == 'member':

            association_key = '_rel_%s' % resource_name
            association_data = self.db[parent.rest_name].find_one({'_id': ObjectId(parent.id)}, {association_key: 1})

            if not association_data or association_key not in association_data:
                return GAStoragePluginQueryResponse(data=[], count=0)

            data = self.db[resource_name].find({'$and': [{'_id': {'$in': [ObjectId(identifier) for identifier in association_data[association_key]]}}, query_filter]})

        else:
            parent_id = parent.id if parent and parent.id else 'none'

            identifiers = self.permissions_controller.child_ids_with_permission(resource=user_identifier,
                                                                                parent_id=parent_id,
                                                                                children_type=resource_name,
                                                                                permission='read')

            data = self.db[resource_name].find({'$and': [{'_id': {'$in': [ObjectId(i) for i in identifiers]}}, query_filter]})

        if not data.count():
            return GAStoragePluginQueryResponse(data=[], count=0)

        if order_by:
            data = data.sort(order_by)

        if grand_total:
            total_count = data.count()
            data = data.skip(skip).limit(page_size)
        else:
            data = data.skip(skip).limit(page_size)
            total_count = data.count()

        return GAStoragePluginQueryResponse(data=data, count=total_count)

    def _validate(self, resource):
        """
        """
        if resource.validate():
            return None

        errors = []
        for property_name, error in resource.errors.iteritems():
            errors.append(GAError(type=GAError.TYPE_CONFLICT, title=error["title"], description=error["description"], property_name=error['remote_name']))
        return errors

    def _convert_to_dbid(self, data):
        """
        """
        if data and data['ID']:
            data['_id'] = ObjectId(data['ID'])
            del data['ID']

        if data and data['creationDate']:
            data['creationDate'] = datetime.utcfromtimestamp(float(data['creationDate']))

        if data and data['lastUpdatedDate']:
            data['lastUpdatedDate'] = datetime.utcfromtimestamp(float(data['lastUpdatedDate']))

        return data

    def _convert_from_dbid(self, data):
        """
        """
        if data:
            data['ID'] = str(data['_id'])
            del data['_id']

        if data and data['creationDate']:
            data['creationDate'] = float(calendar.timegm(data['creationDate'].timetuple()))

        if data and data['lastUpdatedDate']:
            data['lastUpdatedDate'] = float(calendar.timegm(data['lastUpdatedDate'].timetuple()))

        return data

    def _parse_filter(self, filter):  # pragma: no cover
        """
        """
        # @TODO: this is a very stupid predicate parsing implementation

        try:
            components = filter.split(' ')
            attribute = components[0]
            operator = components[1].lower()
            value = components[2]

            # if operator == 'contains': operator = '$in'
            if operator == 'equals':
                operator = '$eq'
            elif operator == 'in':
                operator = '$in'
            elif operator == 'not in':
                operator = '$nin'
            elif operator == '==':
                operator = '$eq'
            elif operator == '!=':
                operator = '$neq'
            elif operator == '>':
                operator = '$gt'
            elif operator == '>=':
                operator = '$gte'
            elif operator == '<':
                operator = '$lt'
            elif operator == '<=':
                operator = '$lte'

            if attribute == 'ID':
                attribute = '_id'
                value = ObjectId(value)

            return {attribute: {operator: value}}
        except:
            return {'$text': {'$search': filter}}
