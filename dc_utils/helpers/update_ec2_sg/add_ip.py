import boto3
import configparser
import getpass
import os
import requests


def _get_config():
    """
    Attempts to read a config file
    """
    config_dir = os.environ.get("XDG_CONFIG_HOME", f"{os.environ['HOME']}/.config")
    config = configparser.ConfigParser()
    config.read(f"{config_dir}/update_ec2_sg/config.ini")
    return config


def _get_client():
    """
    Get a boto3 ec2 client instance
    """
    return boto3.client("ec2")


def _get_security_group():
    config = _get_config()
    security_group_desc = config.get(
        "SETTINGS", "SECURITY_GROUP_DESC", fallback="ssh_from_dc_admins_ips"
    )
    return _get_client().describe_security_groups(
        Filters=[
            {
                "Name": "tag:description",
                "Values": [security_group_desc],
            }
        ]
    )["SecurityGroups"][0]


def _format_ip_address(ip_address):
    """
    Ensure IP address is formatted correctly.
    TODO allow range other formats?
    """
    if not ip_address.endswith("/32"):
        ip_address += "/32"
    return ip_address


def remove_ip_from_security_group(ip_address=None):
    """
    Removes an IP address from the security group ingress rules.
    """
    if not ip_address:
        config = _get_config()
        ip_address = config.get(
            "SETTINGS", "IP_ADDRESS", fallback=requests.get("https://ifconfig.me").text
        )

    return _get_client().revoke_security_group_ingress(
        GroupId=_get_security_group()["GroupId"],
        IpProtocol="tcp",
        FromPort=22,
        ToPort=22,
        CidrIp=_format_ip_address(ip_address),
    )


def add_ip_to_security_group():
    """
    Adds an IP address to the projects SSH admin security groups ingress rules.
    You must have valid AWS credentials configured to run the command. For help
    logging in using SSO see
    https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html.
    TODO add documentation for using config file
    """
    config = _get_config()
    ip_to_add = config.get(
        "SETTINGS", "IP_ADDRESS", fallback=requests.get("https://ifconfig.me").text
    )
    description = config.get("SETTINGS", "DESCRIPTION", fallback=getpass.getuser())

    security_group = _get_security_group()

    ssh_ips = list(
        filter(lambda obj: obj["FromPort"] == 22, security_group["IpPermissions"])
    )[0]["IpRanges"]
    ip_to_remove = list(
        filter(
            lambda obj: obj["Description"] == description,
            ssh_ips,
        )
    )
    if ip_to_remove:
        remove_ip_from_security_group(ip_address=ip_to_remove[0]["CidrIp"])

    return _get_client().authorize_security_group_ingress(
        GroupId=security_group["GroupId"],
        IpPermissions=[
            {
                "FromPort": 22,
                "ToPort": 22,
                "IpProtocol": "tcp",
                "IpRanges": [
                    {
                        "CidrIp": _format_ip_address(ip_to_add),
                        "Description": description,
                    },
                ],
            }
        ],
    )
