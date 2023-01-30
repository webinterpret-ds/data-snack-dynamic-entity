import pytest
from typing import Dict

from src.data_snack_dynamic_entity.validate import (
    validate_entity_templates,
    ValidationError,
)


@pytest.fixture
def entity_templates_wrong_fields() -> Dict:
    return {
        "Car": {
            "properties": {
                "name": {},
                "usage": {"typo": "int"},
                "cost": {"type": "float", "default": {}},
            }
        }
    }


@pytest.fixture
def entity_templates_no_properties() -> Dict:
    return {"Car": {}}


def test_validate_correct_template(entity_templates: Dict) -> None:
    """
    Tests if validation works correctly for a correct template with a single entity
    """
    try:
        validate_entity_templates(entity_templates)
    except ValidationError:
        pytest.fail()


def test_validate_templates_many(entity_templates_many: Dict) -> None:
    """
    Tests if validation works correctly for a correct template with multiple entities
    """
    try:
        validate_entity_templates(entity_templates_many)
    except ValidationError:
        pytest.fail()


def test_validate_template_wrong_field(entity_templates_wrong_fields: Dict) -> None:
    """
    Tests if validation will fail if a template contains wrong fields.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(entity_templates_wrong_fields)


def test_validate_template_no_properties(entity_templates_no_properties: Dict) -> None:
    """
    Tests if validation will fail if a template contains no properties field.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(entity_templates_no_properties)


@pytest.mark.parametrize("dependent_field", ["optional", "default"])
def test_validate_template_key_dependent_fields(dependent_field) -> None:
    """
    Tests if validation will fail if a template contains `key` = `True` and invalid dependent fields.
    """
    schema = {
        "Car": {
            "properties": {
                "index": {"key": True, dependent_field: True}
            }
        }
    }
    with pytest.raises(ValidationError):
        validate_entity_templates(schema)


@pytest.mark.parametrize("field_name", ["key", "optional", "excluded"],)
def test_validate_template_booleans(field_name) -> None:
    """
    Tests if validation will fail if a template contains fields does not follow boolean type directive.
    """
    schema = {
        "Car": {
            "properties": {
                "index": {field_name: "not_bool"}
            }
        }
    }
    with pytest.raises(ValidationError):
        validate_entity_templates(schema)
