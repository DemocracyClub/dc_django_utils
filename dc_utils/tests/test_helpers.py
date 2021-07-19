from dc_utils.tests.helpers import validate_html


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
    tidy_document.assert_called_once_with("html_content")
