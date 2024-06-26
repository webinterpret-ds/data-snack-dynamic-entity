import pytest
from typing import Dict

from data_snack_dynamic_entity.validate import validate_entity_templates, ValidationError


@pytest.fixture
def simple_entity_templates_wrong_fields() -> Dict:
    return {
        "Car": {
            "type": "simple",
            "version": 1,
            "properties": {
                "name": {},
                "usage": {"typo": "int"},
                "cost": {"type": "float", "default": {}},
            }
        }
    }


@pytest.fixture
def simple_entity_templates_no_properties() -> Dict:
    return {
        "Car": {
            "type": "simple",
            "version": 1,
        }
    }


@pytest.fixture
def simple_entity_templates_no_version() -> Dict:
    return {
        "Car": {
            "type": "simple",
            "properties": {
                "name": {},
                "usage": {"typo": "int"},
                "cost": {"type": "float", "default": {}},
            }
        }
    }


@pytest.fixture
def simple_entity_templates_no_type() -> Dict:
    return {
        "Car": {
            "version": 1,
            "properties": {
                "name": {},
                "usage": {"typo": "int"},
                "cost": {"type": "float", "default": {}},
            }
        }
    }


def test_validate_correct_template(simple_entity_templates: Dict) -> None:
    """
    Tests if validation works correctly for a correct template with a single entity
    """
    try:
        validate_entity_templates(simple_entity_templates)
    except ValidationError:
        pytest.fail()


def test_validate_templates_many(simple_entity_templates_many: Dict) -> None:
    """
    Tests if validation works correctly for a correct template with multiple entities
    """
    try:
        validate_entity_templates(simple_entity_templates_many)
    except ValidationError:
        pytest.fail()


def test_validate_template_wrong_field(simple_entity_templates_wrong_fields: Dict) -> None:
    """
    Tests if validation will fail if a template contains wrong fields.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(simple_entity_templates_wrong_fields)


def test_validate_template_no_properties(simple_entity_templates_no_properties: Dict) -> None:
    """
    Tests if validation will fail if a template contains no properties field.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(simple_entity_templates_no_properties)


@pytest.mark.parametrize("dependent_field", ["optional", "default"])
def test_validate_template_key_dependent_fields(dependent_field) -> None:
    """
    Tests if validation will fail if a template contains `key` = `True` and invalid dependent fields.
    """
    schema = {
        "Car": {
            "type": "simple",
            "version": 1,
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
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {field_name: "not_bool"}
            }
        }
    }
    with pytest.raises(ValidationError):
        validate_entity_templates(schema)


def test_validate_version(simple_entity_templates_no_version: Dict) -> None:
    """
    Tests if validation will fail if a template doesn't contain a version.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(simple_entity_templates_no_version)


def test_validate_type(simple_entity_templates_no_type: Dict) -> None:
    """
    Tests if validation will fail if a template doesn't contain a type.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(simple_entity_templates_no_type)
