from typing import Dict
from unittest.mock import patch, MagicMock

import pytest

from data_snack_dynamic_entity.compound_entity.types import CompoundEntityTemplates
from data_snack_dynamic_entity.factory import load_entities
from data_snack_dynamic_entity.simple_entity.types import SimpleEntityTemplates
from data_snack_dynamic_entity.types import EntityTemplates


@pytest.fixture
def simple_entity_templates() -> Dict:
    return {
        "Person": {
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True},
                "name": {"type": "str"},
            }
        },
        "Car": {
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True},
                "brand": {"type": "str"},
            }
        }
    }


@pytest.fixture
def compound_entity_templates() -> Dict:
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
                        },
                        {
                            "field": "brand",
                            "source_field": "brand",
                        }
                    ]
                },
                {
                    "entity": "Person",
                    "fields": [
                        {
                            "field": "person_index",
                            "source_field": "index",
                        },
                        {
                            "field": "name",
                            "source_field": "name",
                        }
                    ]
                }
            ]
        }
    }


@pytest.fixture
def entity_templates() -> Dict:
    return {
        "Person": {
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True},
                "name": {"type": "str"},
            }
        },
        "Car": {
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True},
                "brand": {"type": "str"},
            }
        },
        "Registration": {
            "type": "compound",
            "sources": [
                {
                    "entity": "Car",
                    "fields": [
                        {
                            "field": "car_index",
                            "source_field": "index",
                        },
                        {
                            "field": "brand",
                            "source_field": "brand",
                        }
                    ]
                },
                {
                    "entity": "Person",
                    "fields": [
                        {
                            "field": "person_index",
                            "source_field": "index",
                        },
                        {
                            "field": "name",
                            "source_field": "name",
                        }
                    ]
                }
            ]
        }
    }


@patch('data_snack_dynamic_entity.factory.SimpleEntityFactory.load_entities')
@patch('data_snack_dynamic_entity.factory.CompoundEntityFactory.load_entities')
def test__compound_load_entities__executing_load_entities(
        compound_load_entities_mock: MagicMock,
        simple_load_entities_mock: MagicMock,
        simple_entity_templates: SimpleEntityTemplates,
        compound_entity_templates: CompoundEntityTemplates,
        entity_templates: EntityTemplates,
) -> None:
    source_entities_mock = MagicMock()
    simple_load_entities_mock.return_value = source_entities_mock

    load_entities(entity_templates)

    simple_load_entities_mock.assert_called_with(simple_entity_templates)
    compound_load_entities_mock.assert_called_with(compound_entity_templates, source_entities_mock)
