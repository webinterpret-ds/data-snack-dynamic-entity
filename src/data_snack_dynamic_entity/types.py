from typing import TypedDict, Dict, Union


class FieldSchema(TypedDict):
    type: str
    key: bool
    excluded: bool
    optional: bool
    default: Union[str, int, float, bool]


class EntitySchema(TypedDict):
    properties: Dict[str, FieldSchema]


EntityTemplates = Dict[str, EntitySchema]
