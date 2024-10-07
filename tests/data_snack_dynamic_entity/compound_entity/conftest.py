from dataclasses import dataclass, field

import pytest
from typing import Dict, List, Optional, Type

from attr.validators import optional
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
class CarOwner(Entity):
    index: str
    car_index: str
    name: Optional[str] = field(default=None)

    class Meta:
        keys: List[str] = ["index", "car_index"]
        excluded_fields: List[str] = []
        version = 1


@pytest.fixture
def source_entities() -> Dict[str, Type]:
    return {
        "Car": Car,
        "CarOwner": CarOwner,
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
                    ],
                },
                {
                    "entity": "CarOwner",
                    "fields": [
                        {
                            "field": "person_index",
                            "source_field": "index",
                        },
                        {
                            "field": "car_index",
                            "source_field": "car_index",
                        },
                        {
                            "field": "name",
                            "source_field": "name",
                        }
                    ],
                    "optional": True,
                }
            ]
        }
    }
