import pytest
from typing import Dict


@pytest.fixture
def entity_templates() -> Dict:
    return {
        "Car": {
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
def entity_templates_many() -> Dict:
    return {
        "Cat": {
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True},
                "name": {"type": "str"},
            }
        },
        "Dog": {
            "version": 1,
            "properties": {
                "index": {"type": "int", "key": True},
                "name": {"type": "str"},
            }
        },
    }
