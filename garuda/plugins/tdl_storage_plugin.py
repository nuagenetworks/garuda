# -*- coding: utf-8 -*-

from garuda.core.plugins import GAModelControllerPlugin, GAPluginManifest
from garuda.core.lib import SDKsManager
from uuid import uuid4

class TDLStoragePlugin(GAModelControllerPlugin):
    """
    """

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='TDL Storage',
                                version=1.0,
                                identifier="garuda.plugins.model.tdl")

    def did_register(self):
        """
        """
        self._sdk = SDKsManager().get_sdk("tdldk")
        self._database = {
            "list": [
                {
                    "ID": "1",
                    "title": "Shopping List",
                    "description": "Things to buy"
                },
                {
                    "ID": "2",
                    "title": "Secret List",
                    "description": "You should not see this"
                }
            ],
            "task": [
                {
                        "ID": "11",
                        "parentID": "1",
                        "parentType": "list",
                        "title": "Buy Milk",
                        "description": "because it is good",
                        "status": "TODO"
                    },
                    {
                        "ID": "12",
                        "parentID": "1",
                        "parentType": "list",
                        "title": "Buy Chocolate",
                        "description": "because it is even better",
                        "status": "TODO"
                    },
                    {
                        "ID": "21",
                        "parentID": "2",
                        "parentType": "list",
                        "title": "Explain Monolithe",
                        "description": "We are doing it right now",
                        "status": "TODO"
                    },
                    {
                        "ID": "22",
                        "parentID": "2",
                        "parentType": "list",
                        "title": "Make Garuda popular",
                        "description": "Almost done",
                        "status": "TODO"
                    },
                    {
                        "ID": "23",
                        "parentID": "2",
                        "parentType": "list",
                        "title": "Dominate the world",
                        "description": "That is the plan",
                        "status": "TODO"
                    }
            ],
            "root": [{
                "ID": "root-id-1",
                "userName": "root",
                "password": "password"
            }]
        }

    def should_manage(self, resource_name, identifier):
        """
        """
        return True

    def instantiate(self, resource_name):
        """
        """

        if resource_name == "list":
            return self._sdk.GAList()

        if resource_name == "task":
            return self._sdk.GATask()

        if resource_name == "root":
            return self._sdk.GARoot()

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

        if resource_name == "list":

            for item in self._database["list"]:
                l = self.instantiate("list")
                l.from_dict(item)
                ret.append(l)
        else:

            for item in self._database["task"]:
                if item["parentID"] == parent.id:
                    ret.append(self.get(resource_name, item["ID"]))

        return ret

    def save(self, resource, parent=None):
        """
        """
        resource.id = str(uuid4())

        if not parent:
            self._database["list"].append(resource.to_dict())
        else:
            resource.parent_type = "list"
            resource.parent_id = parent.id
            self._database["task"].append(resource.to_dict())

    def delete(self, resource):
        """
        """
        table = self._database[resource.rest_name]

        for item in table:
            if item["ID"] == resource.id:
                table.remove(item)