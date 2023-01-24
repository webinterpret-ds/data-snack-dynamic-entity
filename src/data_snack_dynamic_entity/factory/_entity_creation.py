from dataclasses import field, make_dataclass
from typing import Type, List, Optional, Callable

from data_snack.entities import Entity

from data_snack_dynamic_entity.types import EntitySchema, FieldSchema


FieldValidator = Callable[[str, FieldSchema], None]


def _gettype(name: str) -> Type:
    t = __builtins__.get(name)
    if isinstance(t, type):
        return t
    raise ValueError(name)


def _create_entity_template(entity_name: str, keys: List[str], excluded_fields: List[str]) -> Type:
    return type(
        f"{entity_name}Template",
        (Entity, ),
        {"Meta": type("Meta", (object, ), {"keys": keys, "excluded_fields": excluded_fields})}
    )


def _create_entity(entity_name: str, entity_schema: EntitySchema, field_validators: List[FieldValidator]) -> Type:
    """
    Creates entity of given name according to given schema.
    :param entity_name: new entity name
    :param entity_schema: new entity schema
    :param field_validators: validators to apply on each entity schema field
    :return: new entity type
    """
    fields = []
    keys = []
    excluded_fields = []
    for field_name, field_schema in entity_schema["properties"].items():
        [validator(field_name, field_schema) for validator in field_validators]
        field_type = _gettype(field_schema["type"])

        if field_schema.get("key"):
            keys.append(field_name)
        if field_schema.get("excluded"):
            excluded_fields.append(field_name)
        if field_schema.get("optional"):
            field_type = Optional[field_type]
        if "default" in field_schema:
            fields.append((field_name, field_type, field(default=field_schema["default"])))
        else:
            fields.append((field_name, field_type))

    entity_template = _create_entity_template(entity_name=entity_name, keys=keys, excluded_fields=excluded_fields)
    return make_dataclass(entity_name, fields, bases=(entity_template,), namespace={"__module__": __name__})


