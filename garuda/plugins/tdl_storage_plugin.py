# -*- coding: utf-8 -*-
from uuid import uuid4
from bambou import NURESTModelController

from garuda.core.plugins import GAModelControllerPlugin, GAPluginManifest
from garuda.core.models import GAError
from garuda.core.lib import SDKsManager

class TDLStoragePlugin(GAModelControllerPlugin):
    """
    """
    MAX_ID = 1

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='TDL SQLite Storage', version=1.0, identifier="garuda.plugins.tdl.storage.sqlite")

    def did_register(self):
        """
        """
        self._sdk = SDKsManager().get_sdk("tdldk")
        self._database = {}

        for models in NURESTModelController.get_all_models():

            model = models[0]

            self._database[model.rest_name] = []

            if model.rest_name == self._sdk.SDKInfo.root_object_class().rest_name:
                self._database[model.rest_name].append({"ID": "0", "userName": "root", "password": "password"})

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
        table = self._database[resource_name]
        obj = self.instantiate(resource_name)

        for item in table:
            if item["ID"] == identifier:
                obj.from_dict(item)
                return obj

    def get_all(self, parent, resource_name):
        """
        """
        ret = []

        for item in self._database[resource_name]:

            obj_id = item["ID"]

            if parent:
                if item["parentID"] == parent.id:
                    ret.append(self.get(resource_name, obj_id))

            else:
                ret.append(self.get(resource_name, obj_id))

        return ret

    def create(self, resource, parent=None):
        """
        """
        validation = self._validate(resource)
        if validation: return validation

        resource.id = str(self.MAX_ID)

        self.MAX_ID += 1

        if parent:
            resource.parent_type = parent.rest_name
            resource.parent_id = parent.id

        self._database[resource.rest_name].append(resource.to_dict())

    def update(self, resource):
        """
        """

        validation = self._validate(resource)
        if validation: return validation

        data = self._get_raw_data(resource.rest_name, resource.id)

        if not data:
            return GAError(type=GAError.TYPE_NOTFOUND, title="Cannot find that shit", description="Wesh no")

        if (resource.__class__(data=data)).rest_equals(resource):
            return GAError(type=GAError.TYPE_CONFLICT, title="No changes to modify the entity", description="There are no attribute changes to modify the entity.")

        data.update(resource.to_dict())

    def delete(self, resource):
        """
        """
        table = self._database[resource.rest_name]

        for item in table:
            if item["ID"] == resource.id:
                table.remove(item)

    def _validate(self, resource):
        """
        """
        if resource.validate():
            return None

        errors = []
        for property_name, error in resource.errors.iteritems():
            errors.append(GAError(type=GAError.TYPE_CONFLICT, title=error["title"], description=error["description"], property_name=property_name))
        return errors

    def _get_raw_data(self, resource_name, identifier):
        """
        """
        table = self._database[resource_name]
        for item in table:
            if item["ID"] == identifier:
                return item