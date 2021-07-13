from tidylib import tidy_document

def validate_html(client):
    response = client.get('/')
    content = response.content
    document, errors = tidy_document(content)
    assert errors == None
    