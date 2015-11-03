{
    "attributes": {
        "description": {
            "description": "the desc", 
            "exposed": true, 
            "filterable": true, 
            "format": "free", 
            "orderable": true, 
            "type": "string"
        }, 
        "name": {
            "description": "the name", 
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
        "user": {
            "get": true, 
            "relationship": "member", 
            "update": true
        }
    }, 
    "model": {
        "delete": true, 
        "entity_name": "Group", 
        "get": true, 
        "resource_name": "groups", 
        "rest_name": "group", 
        "update": true
    }
}