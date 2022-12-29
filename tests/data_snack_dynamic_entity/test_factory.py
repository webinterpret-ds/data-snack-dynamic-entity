import pytest
from data_snack_dynamic_entity import load_entities
from typing import Dict, Type, Union, get_origin, get_args


def _is_optional(field_type: Type) -> bool:
    """
    According to https://stackoverflow.com/questions/56832881/check-if-a-field-is-typing-optional
    this checks if field is Optional
    :param field_type: type of the field
    :returns: true if field is Optional
    """
    return get_origin(field_type) is Union and type(None) in get_args(field_type)


def test_load_entities(entity_templates: Dict) -> None:
    """
    Testing if `load_entities` is correctly parsing template and creating a new type.
    """
    entities = load_entities(entity_templates)

    assert len(entities) == 1

    Car = entities["Car"]
    assert _is_optional(Car.__dataclass_fields__["name"].type) is False
    assert _is_optional(Car.__dataclass_fields__["usage"].type) is True
    assert _is_optional(Car.__dataclass_fields__["cost"].type) is False

    car = Car(name="name", usage=10)
    assert isinstance(car, Car)
    assert car.cost == 0.0

    car = Car(name="name", usage=10, cost=10.0)
    assert car.cost == 10.0


def test_load_entities_many(entity_templates_many: Dict) -> None:
    """
    Testing if `load_entities` works correctly if more than one Entity is defined in the template.
    """
    entities = load_entities(entity_templates_many)

    assert len(entities) == 2
    for Entity in entities.values():
        assert isinstance(Entity, Type)

        obj = Entity(name="test")
        assert isinstance(obj, Entity)


@pytest.fixture
def entity_templates_wrong_field_type() -> Dict:
    return {
        "Car": {
            "properties": {
                "name": {"type": "string"},
            }
        }
    }


def test_load_entities_wrong_field_type(
    entity_templates_wrong_field_type: Dict,
) -> None:
    """
    Testing if using a wrong field type will raise an error
    """
    with pytest.raises(ValueError):
        load_entities(entity_templates_wrong_field_type)
