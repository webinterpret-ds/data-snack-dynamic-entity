import pytest
from typing import Dict


@pytest.fixture
def entity_templates_wrong_fields() -> Dict:
    return {
        'Car': {
            'properties': {
                'name': {},
                'usage': {'typo': 'int'},
                'cost': {'type': 'float', 'default': {}}
            }
        }
    }


@pytest.fixture
def entity_templates_no_properties() -> Dict:
    return {
        'Car': {}
    }
