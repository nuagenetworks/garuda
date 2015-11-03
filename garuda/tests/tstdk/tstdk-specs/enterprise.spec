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
        }, 
        "zipcode": {
            "description": "zip code", 
            "exposed": true, 
            "filterable": true, 
            "format": "free", 
            "orderable": true, 
            "type": "integer"
        }
    }, 
    "children": {
        "group": {
            "create": true, 
            "get": true, 
            "relationship": "child"
        }, 
        "user": {
            "create": true, 
            "get": true, 
            "relationship": "child"
        }
    }, 
    "model": {
        "delete": true, 
        "entity_name": "Enterprise", 
        "get": true, 
        "resource_name": "enterprises", 
        "rest_name": "enterprise", 
        "update": true
    }
}