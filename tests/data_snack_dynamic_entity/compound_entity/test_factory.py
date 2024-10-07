from unittest.mock import MagicMock, patch

import pytest
from typing import Type, Dict

from data_snack.entities.exceptions import SourceEntityFieldException
from data_snack.entities.models import EntityFieldMapping

from data_snack_dynamic_entity.compound_entity.factory import CompoundEntityFactory
from data_snack_dynamic_entity.compound_entity.types import CompoundEntityTemplates
from data_snack_dynamic_entity.compound_entity.exceptions import NonExistingSourceEntityException
from data_snack_dynamic_entity.factory import load_entities
from tests.data_snack_dynamic_entity.compound_entity.conftest import Car, CarOwner
from tests.data_snack_dynamic_entity.utils import _is_optional


@pytest.fixture
def compound_entity_factory() -> CompoundEntityFactory:
    return CompoundEntityFactory()


def test__compound_entity_factory__load_entities(
        compound_entity_factory: CompoundEntityFactory,
        compound_entity_templates: CompoundEntityTemplates,
        source_entities: Dict[str, Type],
) -> None:
    """Testing if `CompoundEntityFactory.load_entities` is correctly parsing template and creating a new type."""
    compound_entities = compound_entity_factory.load_entities(compound_entity_templates, source_entities)

    assert len(compound_entities) == 1

    Registration = compound_entities["Registration"]
    assert _is_optional(Registration.__dataclass_fields__["car_index"].type) is False
    assert _is_optional(Registration.__dataclass_fields__["brand"].type) is True
    assert _is_optional(Registration.__dataclass_fields__["person_index"].type) is False
    assert _is_optional(Registration.__dataclass_fields__["name"].type) is True

    registration = Registration(car_index=1, person_index=2)
    assert isinstance(registration, Registration)
    assert registration.car_index == 1
    assert registration.person_index == 2
    assert registration.brand is None
    assert registration.name is None

    registration = Registration(car_index=1, brand="brand", person_index=2, name="name")
    assert registration.brand == "brand"
    assert registration.name == "name"


def test__compound_entity_factory__load_sources_entities(
        compound_entity_factory: CompoundEntityFactory,
        compound_entity_templates: CompoundEntityTemplates,
        source_entities: Dict[str, Type],
) -> None:
    """Testing if `CompoundEntityFactory.load_entities` is correctly parsing template
    and creating a source field mappings."""
    compound_entities = compound_entity_factory.load_entities(compound_entity_templates, source_entities)
    Registration = compound_entities["Registration"]

    assert len(Registration.Meta.sources) == 2
    assert type(Registration.Meta.sources[0].entity) == type(Car)
    assert type(Registration.Meta.sources[1].entity) == type(CarOwner)

    assert len(Registration.Meta.sources[0].entity_fields_mapping) == 2
    assert Registration.Meta.sources[0].entity_fields_mapping[0] == EntityFieldMapping("car_index", "index")
    assert Registration.Meta.sources[0].entity_fields_mapping[1] == EntityFieldMapping("brand", "brand")

    assert len(Registration.Meta.sources[1].entity_fields_mapping) == 3
    assert Registration.Meta.sources[1].entity_fields_mapping[0] == EntityFieldMapping("person_index", "index")
    assert Registration.Meta.sources[1].entity_fields_mapping[1] == EntityFieldMapping("car_index", "car_index")
    assert Registration.Meta.sources[1].entity_fields_mapping[2] == EntityFieldMapping("name", "name")

    assert Registration.Meta.sources[0].optional == False
    assert Registration.Meta.sources[1].optional == True


def test__compound_entity_factory__load_non_existing_source_entity(
        compound_entity_factory: CompoundEntityFactory, source_entities: Dict[str, Type]
) -> None:
    schema = {
        "Registration": {
            "type": "compound",
            "sources": [
                {
                    "entity": "NonExistingSourceEntity",
                    "fields": [
                        {
                            "source_field": "field",
                            "field": "field"
                        }
                    ]
                }
            ]
        }
    }
    with pytest.raises(NonExistingSourceEntityException):
        compound_entity_factory.load_entities(schema, source_entities)


def test__compound_entity_factory__load_non_existing_source_entity_field(
        compound_entity_factory: CompoundEntityFactory, source_entities: Dict[str, Type]
) -> None:
    schema = {
        "Registration": {
            "type": "compound",
            "sources": [
                {
                    "entity": "Car",
                    "fields": [
                        {
                            "source_field": "NonExistingSourceEntityField",
                            "field": "field"
                        }
                    ]
                }
            ]
        }
    }
    with pytest.raises(SourceEntityFieldException):
        compound_entity_factory.load_entities(schema, source_entities)


@patch('data_snack_dynamic_entity.factory.SimpleEntityFactory.load_entities')
@patch('data_snack_dynamic_entity.factory.CompoundEntityFactory.load_entities')
def test__compound_load_entities__executing_load_entities(
        compound_load_entities_mock: MagicMock,
        simple_load_entities_mock: MagicMock,
        compound_entity_templates: CompoundEntityTemplates,
) -> None:
    source_entities_mock = MagicMock()
    simple_load_entities_mock.return_value = source_entities_mock
    load_entities(compound_entity_templates)
    compound_load_entities_mock.assert_called_with(compound_entity_templates, source_entities_mock)
