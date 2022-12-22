import pytest
from typing import Dict


@pytest.fixture
def entity_templates() -> Dict:
    return {
        'Car': {
            'properties': {
                'name': {'type': 'str'},
                'usage': {'type': 'int', 'optional': True},
                'cost': {'type': 'float', 'default': 0.0}
            }
        }
    }


@pytest.fixture
def entity_templates_many() -> Dict:
    return {
        'Cat': {
            'properties': {
                'name': {'type': 'str'},
            }
        },
        'Dog': {
            'properties': {
                'name': {'type': 'str'},
            }
        }
    }
