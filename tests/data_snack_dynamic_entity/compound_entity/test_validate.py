import pytest
from typing import Dict

from data_snack_dynamic_entity.validate import validate_entity_templates, ValidationError


@pytest.fixture
def compound_entity_templates_missing_required_source_entity_field() -> Dict:
    return {
        "Registration": {
            "type": "compound",
            "sources": [
                {
                    "fields": [
                        {
                            "source_field": "index",
                            "field": "field"
                        },
                    ]
                }
            ]
        }
    }


@pytest.fixture
def compound_entity_templates_missing_required_source_fields() -> Dict:
    return {
        "Registration": {
            "type": "compound",
            "sources": [
                {
                    "entity": "Car",
                }
            ]
        }
    }


@pytest.fixture
def compound_entity_templates_missing_required_field() -> Dict:
    return {
        "Registration": {
            "type": "compound",
            "sources": [
                {
                    "entity": "Car",
                    "fields": [
                        {
                            "source_field": "index"
                        },
                    ]
                }
            ]
        }
    }


@pytest.fixture
def compound_entity_templates_missing_required_source_field() -> Dict:
    return {
        "Registration": {
            "type": "compound",
            "sources": [
                {
                    "entity": "Car",
                    "fields": [
                        {
                            "field": "car_index"
                        },
                    ]
                }
            ]
        }
    }


@pytest.fixture
def compound_entity_templates_wrong_field_types() -> Dict:
    return {
        "Registration": {
            "type": "compound",
            "sources": [
                {
                    "entity": "Car",
                    "fields": [
                        {
                            "field": "car_index",
                            "source_field": 1,
                        },
                        {
                            "field": "brand",
                            "source_field": True,
                        }
                    ]
                }
            ]
        }
    }


@pytest.fixture
def compound_entity_templates_additional_properties() -> Dict:
    return {
        "Registration": {
            "type": "compound",
            "sources": [
                {
                    "entity": "Car",
                    "fields": [
                        {
                            "field": "car_index",
                            "source_field": "index",
                            "additional": "true"
                        }
                    ]
                }
            ]
        }
    }


@pytest.fixture
def compound_entity_templates_no_sources() -> Dict:
    return {
        "Registration": {
            "type": "compound"
        }
    }


@pytest.fixture
def compound_entity_templates_no_type() -> Dict:
    return {
        "Registration": {
            "sources": [],
        }
    }


def test_validate_correct_compound_entity_template(compound_entity_templates: Dict) -> None:
    """
    Tests if validation works correctly for a correct template with a single compound entity
    """
    try:
        validate_entity_templates(compound_entity_templates)
    except ValidationError:
        pytest.fail()


def test_validate_template_missing_required_source_entity_field(
        compound_entity_templates_missing_required_source_entity_field: Dict
) -> None:
    """
    Tests if validation will fail if a template contains missing entity in sources.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(compound_entity_templates_missing_required_source_entity_field)


def test_validate_template_missing_required_source_fields(
        compound_entity_templates_missing_required_source_fields: Dict
) -> None:
    """
    Tests if validation will fail if a template contains missing fields in sources.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(compound_entity_templates_missing_required_source_fields)


def test_validate_template_missing_required_field(compound_entity_templates_missing_required_field: Dict) -> None:
    """
    Tests if validation will fail if a template contains missing source field in fields.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(compound_entity_templates_missing_required_field)


def test_validate_template_missing_required_source_field(
        compound_entity_templates_missing_required_source_field: Dict
) -> None:
    """
    Tests if validation will fail if a template contains missing field in fields.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(compound_entity_templates_missing_required_source_field)


def test_validate_template_wrong_field_types(compound_entity_templates_wrong_field_types: Dict) -> None:
    """
    Tests if validation will fail if a template contains wrong field types.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(compound_entity_templates_wrong_field_types)


def test_validate_template_additional_properties(compound_entity_templates_additional_properties: Dict) -> None:
    """
    Tests if validation will fail if a template contains additional properties field.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(compound_entity_templates_additional_properties)


def test_validate_template_no_type(compound_entity_templates_no_type: Dict) -> None:
    """
    Tests if validation will fail if a template contains no type field.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(compound_entity_templates_no_type)


def test_validate_template_no_sources(compound_entity_templates_no_sources: Dict) -> None:
    """
    Tests if validation will fail if a template contains no sources field.
    """
    with pytest.raises(ValidationError):
        validate_entity_templates(compound_entity_templates_no_sources)
