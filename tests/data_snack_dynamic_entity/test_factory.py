from typing import Dict, Type

from data_snack_dynamic_entity import load_entities


def test_load_entities(entity_templates: Dict) -> None:
    """
    Testing if `load_entities` is correctly parsing template and creating a new type.
    """
    entities = load_entities(entity_templates)

    assert len(entities) == 1

    Car = entities['Car']
    assert isinstance(Car, Type)

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
