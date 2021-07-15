import pytest
from tidylib import tidy_document

@pytest.fixture
def validate_html(client):
    response = client.get('/')
    content = response.content
    document, errors = tidy_document(content)
    assert errors == None
    