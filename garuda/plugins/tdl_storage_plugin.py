# -*- coding: utf-8 -*-
from uuid import uuid4
from bambou import NURESTModelController
import sqlite3
from time import time

from garuda.core.plugins import GAModelControllerPlugin, GAPluginManifest
from garuda.core.models import GAError
from garuda.core.lib import SDKsManager


class TDLStoragePlugin(GAModelControllerPlugin):
    """
    """

    def __init__(self, db_path):
        """
        """
        self._db_path = db_path


    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='TDL SQLite Storage', version=1.0, identifier="garuda.plugins.tdl.storage.sqlite")

    def did_register(self):
        """
        """
        self._database = {}
        self._sdk = SDKsManager().get_sdk("current")

        import os
        db_needs_init = not os.path.exists(self._db_path)

        self._db = sqlite3.connect(self._db_path, check_same_thread=False)
        self._db.row_factory = sqlite3.Row

        if db_needs_init:
            self._initialize_database()

    def _convert_type(self, typ):
        """
        """
        if typ is str: return 'text'
        if typ is float: return 'real'
        if typ is int: return 'integer'
        return 'text'

    def _row_to_dict(self, row):
        """
        """
        ret = {}
        for key in row.keys():
            ret[key] = row[key]
        return ret

    def _ressource_to_attr_arrays(self, resource):
        """
        """
        attrs = []
        values = []
        for attribute in resource.get_attributes():
            attrs.append(attribute.remote_name)
            values.append(getattr(resource, attribute.local_name))
        return (attrs, values)

    def _initialize_database(self):
        """
        """

        for models in NURESTModelController.get_all_models():

            model = models[0]()

            columns = []

            for attribute in model.get_attributes():
                name = attribute.remote_name
                typ = self._convert_type(attribute.attribute_type)

                if name == "ID":
                    columns.append('%s text primary key' % name)
                else:
                    columns.append('%s %s' % (name, typ))

            create_query = 'create table "%s" (%s)' % (model.rest_name, ", ".join(columns))
            self._db.execute(create_query)

            if model.rest_name == self._sdk.SDKInfo.root_object_class().rest_name:
                self._db.execute('insert into %s (ID, userName, password) values ("1", "root", "password")' % model.rest_name)


            # if model.rest_name == self._sdk.SDKInfo.root_object_class().rest_name:
            #     self._db.execute('insert into %s (ID, userName, password, enterpriseID) values ("1", "root", "password", "2")' % model.rest_name)
            #
            # if model.rest_name == "enterprise":
            #     self._db.execute('insert into %s (ID, name) values ("2", "csp")' % model.rest_name)
            #
            # if model.rest_name == "systemconfig":
            #     self._db.execute('insert into %s (ID) values ("3")' % model.rest_name)

        self._db.commit()

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
        c = self._db.cursor()
        c.execute('select * from "%s" where ID=?' % resource_name, (identifier,))

        row = c.fetchone()

        if not row:
            return None

        obj = self.instantiate(resource_name)
        obj.from_dict(self._row_to_dict(row))

        return obj

    def get_all(self, parent, resource_name):
        """
        """
        ret = []

        c = self._db.cursor()

        if parent:
            print parent.id
            c.execute('select * from "%s" where parentID=?' % resource_name, (parent.id,))
        else:
            c.execute('select * from "%s"' % resource_name)

        for row in c.fetchall():
            obj = self.instantiate(resource_name)
            obj.from_dict(self._row_to_dict(row))
            ret.append(obj)

        print ret
        return ret

    def create(self, resource, parent=None):
        """
        """
        resource.last_updated_date = "now"
        resource.last_updated_by = "me"
        resource.owner = "me"

        validation = self._validate(resource)
        if validation: return validation

        resource.id = str(uuid4())

        if parent:
            resource.parent_type = parent.rest_name
            resource.parent_id = parent.id

        attrs, values = self._ressource_to_attr_arrays(resource)

        insert_query = 'insert into "%s" (%s) values (%s)' % (resource.rest_name, ", ".join(attrs), ", ".join(["?" for v in values]))

        try:
            self._db.execute(insert_query, values)
        except:

            print insert_query
            print values
            print values[16]
            raise

        self._db.commit()

    def update(self, resource):
        """
        """

        resource.last_updated_date = "now"
        resource.last_updated_by = "me"

        validation = self._validate(resource)
        if validation: return validation

        current_obj = self.get(resource.rest_name, resource.id)

        if current_obj.rest_equals(resource):
            return GAError(type=GAError.TYPE_CONFLICT, title="No changes to modify the entity", description="There are no attribute changes to modify the entity.")

        attrs, values = self._ressource_to_attr_arrays(resource)

        vals = []
        for attr in attrs:
            vals.append("%s=?" % attr)

        update_query = 'update "%s" set %s where ID=?' % (resource.rest_name, ", ".join(vals))

        values.append(resource.id)
        self._db.execute(update_query, values)
        self._db.commit()

    def delete(self, resource):
        """
        """

        delete_query = 'delete from "%s" where ID=?' % (resource.rest_name)
        self._db.execute(delete_query, (resource.id,))
        self._db.commit()


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