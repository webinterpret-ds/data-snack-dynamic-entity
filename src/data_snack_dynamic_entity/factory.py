from collections import defaultdict
from typing import Dict, Any, Type, Tuple

from data_snack_dynamic_entity.compound_entity.factory import CompoundEntityFactory
from data_snack_dynamic_entity.compound_entity.types import CompoundEntityTemplates
from data_snack_dynamic_entity.simple_entity.factory import SimpleEntityFactory
from data_snack_dynamic_entity.simple_entity.types import SimpleEntityTemplates
from data_snack_dynamic_entity.types import EntityTemplates


def split_templates_by_type(templates: EntityTemplates) -> Tuple[SimpleEntityTemplates, CompoundEntityTemplates]:
    templates_types = defaultdict(dict)
    for entity_name, entity_schema in templates.items():
        templates_types[entity_schema["type"]].update({entity_name: entity_schema})
    return templates_types["simple"], templates_types["compound"]


def load_entities(templates: EntityTemplates, types_mapping: Dict[str, Any] = None) -> Dict[str, Type]:
    if not types_mapping:
        types_mapping = {}

    simple_entities_templates, compound_entities_templates = split_templates_by_type(templates)
    simple_entities = SimpleEntityFactory(types_mapping).load_entities(simple_entities_templates)
    compound_entities = CompoundEntityFactory().load_entities(compound_entities_templates, simple_entities)
    return {**simple_entities, **compound_entities}

