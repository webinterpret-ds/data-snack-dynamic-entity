import pytest
from typing import Dict


@pytest.fixture
def simple_entity_templates() -> Dict:
    return {
        "Car": {
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True},
                "excluded": {"type": "int", "excluded": True},
                "name": {"type": "str"},
                "usage": {"type": "int", "optional": True},
                "cost": {"type": "float", "default": 0.0},
            }
        }
    }


@pytest.fixture
def simple_entity_templates_many() -> Dict:
    return {
        "Cat": {
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True},
                "name": {"type": "str"},
            }
        },
        "Dog": {
            "type": "simple",
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True},
                "name": {"type": "str"},
            }
        },
    }
