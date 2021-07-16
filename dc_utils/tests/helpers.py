from tidylib import tidy_document

def validate_html(client, url):
    """
    Fixture that can be used to help test html is valid.
    """
    response = client.get(url)
    content = response.content
    document, errors = tidy_document(content)
    return document, errors
