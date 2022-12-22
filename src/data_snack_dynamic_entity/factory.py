from dataclasses import make_dataclass, field
from data_snack.entities import Entity
from typing import Type, Text, Dict, Optional

from .validate import validate_entity_templates


def _gettype(name: Text) -> Type:
    t = __builtins__.get(name)
    if isinstance(t, type):
        return t
    raise ValueError(name)


def _create_entity(entity_name: Text, entity_schema: Dict) -> Entity:
    fields = []
    for field_name, field_schema in entity_schema['properties'].items():
        field_type = _gettype(field_schema['type'])
        if field_schema.get('optional'):
            field_type = Optional[field_type]
        if 'default' in field_schema:
            fields.append((field_name, field_type, field(default=field_schema['default'])))
        else:
            fields.append((field_name, field_type))
    return make_dataclass(entity_name, fields, bases=(Entity,))


def load_entities(templates: Dict) -> Dict[Text, Entity]:
    """
    Creates new Entity types based on provided config.
    Config should contain a valid template that is created according to the schema (see README).

    :param templates: input config containing templates
    :returns: a dictionary with all created Entity types
    """
    validate_entity_templates(templates)
    return {
        entity_name: _create_entity(entity_name, entity_schema)
        for entity_name, entity_schema in templates.items()
    }
