def test_basic_auth(client, settings):
    settings.BASIC_AUTH_ENABLED = True
    assert client.get("/").status_code == 401
    assert (
        client.get("/", HTTP_AUTHORIZATION="Basic ZGM6ZGM=").status_code == 200
    )


def test_basic_auth_disabled(client, settings):
    settings.BASIC_AUTH_ENABLED = False
    assert client.get("/").status_code == 200
