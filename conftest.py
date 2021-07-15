import pytest
from tidylib import tidy_document

@pytest.fixture
def validate_html(client):
    """
    Fixture that can be used to help test html is valid.
    """
    def _test_url(url):
        response = client.get(url)
        content = response.content
        _, errors = tidy_document(content)
        assert errors == None
    
    return _test_url
