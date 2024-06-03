import numpy as np
import pytest
from unittest.mock import MagicMock
from data_snack.entities import Entity
from typing import Type, get_type_hints
from unittest.mock import patch

from data_snack_dynamic_entity.factory import load_entities
from data_snack_dynamic_entity.simple_entity.factory import SimpleEntityFactory
from data_snack_dynamic_entity.simple_entity.types import SimpleEntityTemplates
from tests.data_snack_dynamic_entity.utils import _is_optional


@pytest.fixture
def simple_entity_factory() -> SimpleEntityFactory:
    return SimpleEntityFactory()


@pytest.fixture
def simple_entity_factory_with_mapping() -> SimpleEntityFactory:
    return SimpleEntityFactory({
        "numpy.float16": np.float16
    })


def test__simple_entity_factory__load_entities(
        simple_entity_factory: SimpleEntityFactory, simple_entity_templates: SimpleEntityTemplates
) -> None:
    """Testing if `EntityFactory.load_entities` is correctly parsing template and creating a new type."""
    entities = simple_entity_factory.load_entities(simple_entity_templates)

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
    assert car.Meta.version == 1

    car = Car(index=1, excluded=2, name="name", usage=10, cost=10.0)
    assert car.cost == 10.0


def test__simple_entity_factory__load_entities_many(
        simple_entity_factory: SimpleEntityFactory, simple_entity_templates_many: SimpleEntityTemplates
) -> None:
    """Testing if `load_entities` works correctly if more than one Entity is defined in the template."""
    entities = simple_entity_factory.load_entities(simple_entity_templates_many)

    assert len(entities) == 2
    for entity in entities.values():
        assert isinstance(entity, Type)

        obj = entity(index=1, name="test")
        assert isinstance(obj, Entity)


def test__simple_entity_factory__wrong_builtin_type(simple_entity_factory: SimpleEntityFactory) -> None:
    """Testing if `load_entities` works correctly if more than one Entity is defined in the template."""
    schema = {
        "Car": {
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {"type": "next"},  # needs to be specified according to `EntityClassMeta`
            }
        }
    }
    with pytest.raises(ValueError):
        simple_entity_factory.load_entities(schema)


def test__simple_entity_factory__load_entities_default_values(
        simple_entity_factory: SimpleEntityFactory
) -> None:
    """
    Testing if default values of fields are assigned as expected (key = False, optional = False, excluded = False).
    """
    schema = {
        "Car": {
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True},  # needs to be specified according to `EntityClassMeta`
                "tested_field": {"type": "int"}  # should have key = False, optional = False, excluded = False
            }
        }
    }
    entities = simple_entity_factory.load_entities(schema)
    Car = entities["Car"]
    assert get_type_hints(Car)["tested_field"] is int
    assert Car.get_keys() == ["index"]
    assert not Car.get_excluded_fields()
    assert Car.get_fields() == ["index", "tested_field"]


def test__simple_entity_factory__load_entities_fields_ordering(simple_entity_factory: SimpleEntityFactory) -> None:
    """
    Testing if fields are properly ordered during creation - the default ones should be at the end due to python syntax
    limitations. Scenario simplifies to successful entity creation even if fields with defaults are defined before
    the ones without defaults.
    """
    schema = {
        "Car": {
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True},
                "field_with_default": {"type": "int", "default": 10},
                "field_without_default": {"type": "int"}
            }
        }
    }
    entities = simple_entity_factory.load_entities(schema)
    Car = entities["Car"]
    assert Car


def test__simple_entity_factory__load_entities_excluded_key(simple_entity_factory: SimpleEntityFactory) -> None:
    """
    Testing if key can be excluded
    """
    schema = {
        "Car": {
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True, "excluded": True},
                "other_field": {"type": "int"}
            }
        }
    }
    entities = simple_entity_factory.load_entities(schema)
    Car = entities["Car"]
    assert Car.get_keys() == ["index"]
    assert Car.get_excluded_fields() == ["index"]
    assert Car.get_fields() == ["other_field"]


def test__simple_entity_factory__load_entities_with_types_mappings(
        simple_entity_factory_with_mapping: SimpleEntityFactory
) -> None:
    """
    Testing if key can be excluded
    """
    schema = {
        "Car": {
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True, "excluded": True},
                "numpy_field": {"type": "numpy.float16"}
            }
        }
    }
    entities = simple_entity_factory_with_mapping.load_entities(schema)
    Car = entities["Car"]
    assert Car.get_keys() == ["index"]
    assert Car.get_excluded_fields() == ["index"]
    assert Car.get_fields() == ["numpy_field"]
    assert get_type_hints(Car)["numpy_field"] is np.float16


@patch('data_snack_dynamic_entity.factory.SimpleEntityFactory')
def test__load_entities__passing_types_mapping(
        simple_entity_factory_mock: MagicMock,
        simple_entity_templates: SimpleEntityTemplates
):
    types_mapping = {"numpy.float16": np.float16}
    load_entities(simple_entity_templates, types_mapping)
    simple_entity_factory_mock.assert_called_with(types_mapping)


@patch('data_snack_dynamic_entity.factory.SimpleEntityFactory')
def test__load_entities__default_types_mapping(
        simple_entity_factory_mock: MagicMock,
        simple_entity_templates: SimpleEntityTemplates
):
    load_entities(simple_entity_templates)
    simple_entity_factory_mock.assert_called_with({})


@patch('data_snack_dynamic_entity.factory.SimpleEntityFactory.load_entities')
def test__load_entities__executing_load_entities(
        load_entities_mock: MagicMock,
        simple_entity_templates: SimpleEntityTemplates
):
    load_entities(simple_entity_templates, {})
    load_entities_mock.assert_called_with(simple_entity_templates)
