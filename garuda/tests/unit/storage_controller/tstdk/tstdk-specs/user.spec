{
    "attributes": {
        "fullName": {
            "description": "the full name",
            "exposed": true,
            "filterable": true,
            "format": "free",
            "orderable": true,
            "type": "string"
        },
        "username": {
            "description": "the username",
            "exposed": true,
            "filterable": true,
            "format": "free",
            "orderable": true,
            "required": true,
            "type": "string",
            "unique": true
        }
    },
    "children": {
        "address": {
            "create": true,
            "get": true,
            "relationship": "child"
        },
    },
    "model": {
        "delete": true,
        "entity_name": "User",
        "get": true,
        "resource_name": "users",
        "rest_name": "user",
        "update": true
    }
}