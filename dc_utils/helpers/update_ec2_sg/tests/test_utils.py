import boto3
import os
import pytest

from botocore.exceptions import BotoCoreError
import requests

from .. import utils


class TestGetClient:
    def test_inconfigured_client_error_raised(self, mocker):
        mocker.patch.object(boto3, "client", side_effect=BotoCoreError)
        with pytest.raises(utils.InitBoto3ClientError):
            utils.get_client()

    def test_client_returned(self, mocker):
        mocker.patch.object(boto3, "client", return_value="client_obj")
        assert utils.get_client() == "client_obj"
        boto3.client.assert_called_once_with("ec2")


class TestGetConfig:
    def test_uses_env_var_path(self, mocker):
        os.environ["XDG_CONFIG_HOME"] = "/foo/bar"
        mock_read = mocker.Mock()
        mocker.patch("configparser.ConfigParser.read", mock_read)

        utils.get_config()
        mock_read.assert_called_once_with("/foo/bar/update_ec2_sg/config.ini")
        os.environ.pop("XDG_CONFIG_HOME")

    def test_uses_home_path(self, mocker):
        os.environ["HOME"] = "/home/dir"
        mock_read = mocker.Mock()
        mocker.patch("configparser.ConfigParser.read", mock_read)

        utils.get_config()
        mock_read.assert_called_once_with(f"/home/dir/.config/update_ec2_sg/config.ini")


class TestFormatIPAddress:
    @pytest.mark.parametrize("ip", ["123.123.123", "123.123.123/32"])
    def test_appends_trailing_digits(self, ip):
        assert utils.format_ip_address(ip) == "123.123.123/32"


class TestRemoveIPAddressFromSecurityGroup:
    @pytest.fixture(autouse=True)
    def mock_config(self, mocker):
        mock_config = mocker.Mock()
        mock_config.get.return_value = "123.123.123"
        utils.get_config = mocker.Mock(return_value=mock_config)
        return mock_config

    @pytest.fixture
    def mock_client(self, mocker):
        mock_client = mocker.Mock()
        mock_client.revoke_security_group_ingress.return_value = "revoked"
        utils.get_client = mocker.Mock(return_value=mock_client)
        return mock_client

    @pytest.fixture(autouse=True)
    def mock_security_group(self, mocker):
        utils.get_security_group = mocker.Mock(return_value={"GroupId": "foo1234"})

    def test_defaults_to_config(self, mock_client):

        assert utils.remove_ip_from_security_group(ip_address=None) == "revoked"
        utils.get_config.assert_called_once()
        utils.get_client.assert_called_once()
        mock_client.revoke_security_group_ingress.assert_called_once_with(
            GroupId="foo1234",
            IpProtocol="tcp",
            FromPort=22,
            ToPort=22,
            CidrIp="123.123.123/32",
        )

    def test_config_not_used_when_ip_specified(self, mock_client):
        ip_address = "123.456.789/32"
        assert utils.remove_ip_from_security_group(ip_address=ip_address) == "revoked"
        utils.get_config.assert_not_called()
        utils.get_client.assert_called_once()
        mock_client.revoke_security_group_ingress.assert_called_once_with(
            GroupId="foo1234",
            IpProtocol="tcp",
            FromPort=22,
            ToPort=22,
            CidrIp=ip_address,
        )


class TestAddIPToSecurityGroup:
    @pytest.fixture(autouse=True)
    def mock_remove_ip_from_security_group(self, mocker):
        utils.remove_ip_from_security_group = mocker.Mock()

    @pytest.fixture
    def mock_client(self, mocker):
        mock_client = mocker.Mock()
        mock_client.authorize_security_group_ingress.return_value = "authorized"
        utils.get_client = mocker.Mock(return_value=mock_client)
        return mock_client

    def test_ip_removed_then_added(self, mock_client, mocker):
        mock_config = mocker.Mock()
        mock_config.get.side_effect = ["123.123.123", "joebloggs"]

        utils.get_security_group = mocker.Mock(
            return_value={
                "GroupId": "foo1234",
                "IpPermissions": [
                    {
                        "FromPort": 22,
                        "IpProtocol": "tcp",
                        "IpRanges": [
                            {"CidrIp": "123.123.123/32", "Description": "joebloggs"},
                        ],
                    }
                ],
            }
        )

        utils.get_config = mocker.Mock(return_value=mock_config)

        assert utils.add_ip_to_security_group() == "authorized"
        utils.remove_ip_from_security_group.assert_called_once_with(
            ip_address="123.123.123/32"
        )
        mock_client.authorize_security_group_ingress.assert_called_once_with(
            GroupId="foo1234",
            IpPermissions=[
                {
                    "FromPort": 22,
                    "ToPort": 22,
                    "IpProtocol": "tcp",
                    "IpRanges": [
                        {
                            "CidrIp": "123.123.123/32",
                            "Description": "joebloggs",
                        },
                    ],
                }
            ],
        )

    def test_new_ip_remove_not_called(self, mock_client, mocker):
        mock_config = mocker.Mock()
        mock_config.get.side_effect = ["456.456.456", "newuser"]
        utils.get_config = mocker.Mock(return_value=mock_config)
        assert utils.add_ip_to_security_group() == "authorized"

        utils.remove_ip_from_security_group.assert_not_called()
        mock_client.authorize_security_group_ingress.assert_called_once_with(
            GroupId="foo1234",
            IpPermissions=[
                {
                    "FromPort": 22,
                    "ToPort": 22,
                    "IpProtocol": "tcp",
                    "IpRanges": [
                        {
                            "CidrIp": "456.456.456/32",
                            "Description": "newuser",
                        },
                    ],
                }
            ],
        )

    def test_with_no_existing_ip_permissions(self, mock_client, mocker):
        mock_config = mocker.Mock()
        mock_config.get.side_effect = ["123.123.123", "joebloggs"]
        utils.get_config = mocker.Mock(return_value=mock_config)
        utils.get_security_group = mocker.Mock(
            return_value={
                "GroupId": "foo1234",
                "IpPermissions": [],
            }
        )

        assert utils.add_ip_to_security_group() == "authorized"
        utils.remove_ip_from_security_group.assert_not_called()
        mock_client.authorize_security_group_ingress.assert_called_once_with(
            GroupId="foo1234",
            IpPermissions=[
                {
                    "FromPort": 22,
                    "ToPort": 22,
                    "IpProtocol": "tcp",
                    "IpRanges": [
                        {
                            "CidrIp": "123.123.123/32",
                            "Description": "joebloggs",
                        },
                    ],
                }
            ],
        )

    def test_get_ip_address(self, mocker):
        mocker.patch.object(
            requests, "get", return_value=mocker.Mock(text="123.123.123")
        )
        assert utils.get_ip_address() == "123.123.123"
        requests.get.assert_called_once_with("https://ifconfig.me")
