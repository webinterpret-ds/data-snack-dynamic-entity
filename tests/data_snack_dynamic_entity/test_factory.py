import numpy as np
import pytest
from unittest.mock import MagicMock
from data_snack.entities import Entity
from typing import Dict, Any, Type, Union, get_origin, get_args, get_type_hints
from unittest.mock import patch

from data_snack_dynamic_entity import load_entities
from data_snack_dynamic_entity.factory import EntityFactory
from data_snack_dynamic_entity.types import EntityTemplates


@pytest.fixture
def entity_factory() -> EntityFactory:
    return EntityFactory()


@pytest.fixture
def entity_factory_with_mapping() -> EntityFactory:
    return EntityFactory({
        "numpy.float16": np.float16
    })


def _is_optional(field_type: Type) -> bool:
    """
    According to https://stackoverflow.com/questions/56832881/check-if-a-field-is-typing-optional
    this checks if field is Optional
    :param field_type: type of the field
    :returns: true if field is Optional
    """
    return get_origin(field_type) is Union and type(None) in get_args(field_type)


def test__entity_factory__load_entities(
        entity_factory: EntityFactory, entity_templates: EntityTemplates
) -> None:
    """Testing if `EntityFactory.load_entities` is correctly parsing template and creating a new type."""
    entities = entity_factory.load_entities(entity_templates)

    assert len(entities) == 1

    Car = entities["Car"]
    assert _is_optional(Car.__dataclass_fields__["index"].type) is False
    assert _is_optional(Car.__dataclass_fields__["excluded"].type) is False
    assert _is_optional(Car.__dataclass_fields__["name"].type) is False
    assert _is_optional(Car.__dataclass_fields__["usage"].type) is True
    assert _is_optional(Car.__dataclass_fields__["cost"].type) is False

    car = Car(index=1, excluded=2, name="name", usage=10)
    assert isinstance(car, Car)
    assert car.cost == 0.0
    assert car.Meta.keys == ["index"]
    assert car.Meta.excluded_fields == ["excluded"]

    car = Car(index=1, excluded=2, name="name", usage=10, cost=10.0)
    assert car.cost == 10.0


def test_entity_factory__load_entities_many(
        entity_factory: EntityFactory, entity_templates_many: EntityTemplates
) -> None:
    """Testing if `load_entities` works correctly if more than one Entity is defined in the template."""
    entities = entity_factory.load_entities(entity_templates_many)

    assert len(entities) == 2
    for entity in entities.values():
        assert isinstance(entity, Type)

        obj = entity(index=1, name="test")
        assert isinstance(obj, Entity)


def test__entity_factory__load_entities_default_values(
        entity_factory: EntityFactory
) -> None:
    """
    Testing if default values of fields are assigned as expected (key = False, optional = False, excluded = False).
    """
    schema = {
        "Car": {
            "properties": {
                "index": {"type": "int", "key": True},  # needs to be specified according to `EntityClassMeta`
                "tested_field": {"type": "int"}  # should have key = False, optional = False, excluded = False
            }
        }
    }
    entities = entity_factory.load_entities(schema)
    Car = entities["Car"]
    assert get_type_hints(Car)["tested_field"] is int
    assert Car.get_keys() == ["index"]
    assert not Car.get_excluded_fields()
    assert Car.get_fields() == ["index", "tested_field"]


def test__entity_factory__load_entities_fields_ordering(entity_factory: EntityFactory) -> None:
    """
    Testing if fields are properly ordered during creation - the default ones should be at the end due to python syntax
    limitations. Scenario simplifies to successful entity creation even if fields with defaults are defined before
    the ones without defaults.
    """
    schema = {
        "Car": {
            "properties": {
                "index": {"type": "int", "key": True},
                "field_with_default": {"type": "int", "default": 10},
                "field_without_default": {"type": "int"}
            }
        }
    }
    entities = entity_factory.load_entities(schema)
    Car = entities["Car"]
    assert Car


def test__entity_factory__load_entities_excluded_key(entity_factory) -> None:
    """
    Testing if key can be excluded
    """
    schema = {
        "Car": {
            "properties": {
                "index": {"type": "int", "key": True, "excluded": True},
                "other_field": {"type": "int"}
            }
        }
    }
    entities = entity_factory.load_entities(schema)
    Car = entities["Car"]
    assert Car.get_keys() == ["index"]
    assert Car.get_excluded_fields() == ["index"]
    assert Car.get_fields() == ["other_field"]


def test__entity_factory__load_entities_with_types_mappings(entity_factory_with_mapping: EntityFactory) -> None:
    """
    Testing if key can be excluded
    """
    schema = {
        "Car": {
            "properties": {
                "index": {"type": "int", "key": True, "excluded": True},
                "numpy_field": {"type": "numpy.float16"}
            }
        }
    }
    entities = entity_factory_with_mapping.load_entities(schema)
    Car = entities["Car"]
    assert Car.get_keys() == ["index"]
    assert Car.get_excluded_fields() == ["index"]
    assert Car.get_fields() == ["numpy_field"]
    assert get_type_hints(Car)["numpy_field"] is np.float16


@patch('data_snack_dynamic_entity.factory.EntityFactory')
def test__load_entities__passing_types_mapping(
        entity_factory_mock: MagicMock,
        entity_templates: EntityTemplates
):
    types_mapping = {"numpy.float16": np.float16}
    load_entities(entity_templates, types_mapping)
    entity_factory_mock.assert_called_with(types_mapping)


@patch('data_snack_dynamic_entity.factory.EntityFactory.load_entities')
def test__load_entities__executing_load_entities(
        load_entities_mock: MagicMock,
        entity_templates: EntityTemplates
):
    load_entities(entity_templates, {})
    load_entities_mock.assert_called_with(entity_templates)
