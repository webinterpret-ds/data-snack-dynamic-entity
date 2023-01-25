from data_snack.entities import Entity

from data_snack_dynamic_entity import load_entities
from typing import Type, Union, get_origin, get_args, get_type_hints

from data_snack_dynamic_entity.types import EntityTemplates


def _is_optional(field_type: Type) -> bool:
    """
    According to https://stackoverflow.com/questions/56832881/check-if-a-field-is-typing-optional
    this checks if field is Optional
    :param field_type: type of the field
    :returns: true if field is Optional
    """
    return get_origin(field_type) is Union and type(None) in get_args(field_type)


def test_load_entities(entity_templates: EntityTemplates) -> None:
    """Testing if `load_entities` is correctly parsing template and creating a new type."""
    entities = load_entities(entity_templates)

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


def test_load_entities_many(entity_templates_many: EntityTemplates) -> None:
    """Testing if `load_entities` works correctly if more than one Entity is defined in the template."""
    entities = load_entities(entity_templates_many)

    assert len(entities) == 2
    for entity in entities.values():
        assert isinstance(entity, Type)

        obj = entity(index=1, name="test")
        assert isinstance(obj, Entity)


def test_load_entities_default_values() -> None:
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
    entities = load_entities(schema)
    Car = entities["Car"]
    assert get_type_hints(Car)["tested_field"] is int
    assert Car.get_keys() == ["index"]
    assert not Car.get_excluded_fields()
    assert Car.get_fields() == ["index", "tested_field"]


def test_load_entities_fields_ordering() -> None:
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
    entities = load_entities(schema)
    Car = entities["Car"]
    assert Car

