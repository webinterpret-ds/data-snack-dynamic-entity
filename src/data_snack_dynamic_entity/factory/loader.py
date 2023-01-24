from functools import partial
from typing import Dict, Type

from data_snack_dynamic_entity.validate import validate_entity_templates

from data_snack_dynamic_entity.factory._entity_creation import _create_entity

from data_snack_dynamic_entity.types import EntityTemplates

from data_snack_dynamic_entity.factory._field_validation import (
    key_exclusion_validator,
    key_default_validator,
    key_optionality_validator
)


def load_entities(templates: EntityTemplates) -> Dict[str, Type]:
    """
    Creates new Entity types based on provided config.
    Config should contain a valid template that is created according to the schema (see README).

    :param templates: input config containing templates
    :returns: a dictionary with all created Entity types
    """
    create_entity = partial(
        _create_entity, field_validators=[key_exclusion_validator, key_default_validator, key_optionality_validator]
    )

    validate_entity_templates(templates)
    return {
        entity_name: create_entity(entity_name, entity_schema)
        for entity_name, entity_schema in templates.items()
    }
