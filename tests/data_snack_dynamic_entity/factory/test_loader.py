import pytest
from data_snack.entities import Entity

from data_snack_dynamic_entity import load_entities
from typing import Type, Union, get_origin, get_args

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


def test_load_entities_wrong_field_type() -> None:
    """Testing if using a wrong field type will raise an error."""
    with pytest.raises(ValueError):
        load_entities({"Car": {"properties": {"name": {"type": "string"}, "index": {"type": "int", "key": True}}}})


def test_load_entities_excluded_key() -> None:
    """Testing if using a field marked as key and excluded will raise an error."""
    with pytest.raises(ValueError, match=r"Key can not be excluded.$"):
        load_entities({"Car": {"properties": {"index": {"type": "int", "key": True, "excluded": True}}}})


def test_load_entities_key_with_default() -> None:
    """Testing if using a field marked as key with default will raise an error."""
    with pytest.raises(ValueError, match=r"Key can not have default value."):
        load_entities({"Car": {"properties": {"index": {"type": "int", "key": True, "default": 1}}}})


def test_load_entities_optional_key() -> None:
    """Testing if using a field marked as key and optional will raise an error."""
    with pytest.raises(ValueError, match=r"Key can not be optional."):
        load_entities({"Car": {"properties": {"index": {"type": "int", "key": True, "optional": True}}}})
