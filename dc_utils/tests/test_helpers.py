from dc_utils.tests.helpers import validate_html_str, validate_html


def test_validate_html_str():
    document, errors = validate_html_str(
        """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <title>Hello, world!</title>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <meta name="description" content="" />
    </head>
    <body>
      <h1>Hello, world!</h1>
    </body>
    </html>"""
    )
    assert document == "<h1>\n  Hello, world!\n</h1>\n"
    assert errors == ""


def test_validate_html(mocker):
    """
    - Replace client with mock, and patch tidylib
    - Test that the client is called with the given url
    - Test that tidy_document is called with the html content returned
    by the client
    """
    client = mocker.MagicMock()
    client.get.return_value.content = "html_content"
    tidy_document = mocker.MagicMock(return_value=("document", "errors"))

    mocker.patch("dc_utils.tests.helpers.tidy_document", new=tidy_document)
    url = "/example/"
    result = validate_html(client=client, url=url)

    assert result == ("document", "errors")
    client.get.assert_called_once_with(url)
    tidy_document.assert_called_once_with(
        "html_content",
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
