from tidylib import tidy_document


def validate_html(client, url):
    response = client.get(url)
    content = response.content
    document, errors = validate_html_str(content)
    return document, errors


def validate_html_str(content):
    """
    Helper function that can be used to help test html is valid.
    """
    document, errors = tidy_document(
        content,
        options={
            "indent": 1,  # Pretty; not too much of a performance hit
            "tidy-mark": 0,  # No tidy meta tag in output
            "wrap": 72,  # No wrapping
            "alt-text": "",  # Help ensure validation
            "force-output": 1,  # May not get what you expect but you will get something
            "show-warnings": 0,
            "show-errors": 1,
            "ascii-chars": 1,
            "accessibility-check": 0,  # This is something we may want to turn on once we sort all html failures
            "show-body-only": 1,
            "fix-uri": 0,
            "mute-id": 1,
        },
    )
    return document, errors
