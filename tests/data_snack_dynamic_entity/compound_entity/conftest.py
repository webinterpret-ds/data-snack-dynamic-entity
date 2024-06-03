from dataclasses import dataclass, field

import pytest
from typing import Dict, List, Optional, Type

from data_snack.entities import Entity


@dataclass
class Car(Entity):
    index: str
    brand: Optional[str] = field(default=None)

    class Meta:
        keys: List[str] = ["index"]
        excluded_fields: List[str] = []
        version = 1


@dataclass
class Person(Entity):
    index: str
    name: Optional[str] = field(default=None)

    class Meta:
        keys: List[str] = ["index"]
        excluded_fields: List[str] = []
        version = 1


@pytest.fixture
def source_entities() -> Dict[str, Type]:
    return {
        "Car": Car,
        "Person": Person,
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
