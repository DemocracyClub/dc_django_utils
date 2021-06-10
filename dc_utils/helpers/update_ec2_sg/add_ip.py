import boto3
import configparser
import getpass
import os
import requests


def get_config():
    config_dir = os.environ.get("XDG_CONFIG_HOME", f"{os.environ['HOME']}/.config")
    config = configparser.ConfigParser()
    config.read(f"{config_dir}/update_ec2_sg/config.ini")
    return config

def add_ip_to_security_group():
    """
    Adds an IP address to the projects SSH admin security groups ingress rules.
    You must have valid AWS credentials configured to run the command. For help
    logging in using SSO see 
    https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html.
    TODO add documentation for using config file
    """
    config = get_config()    
    ip_to_add = config.get("SETTINGS", "IP_ADDRESS", fallback=requests.get("https://ifconfig.me").text)
    description = config.get("SETTINGS", "DESCRIPTION", fallback=getpass.getuser())
    security_group_desc = config.get("SETTINGS", "SECURITY_GROUP_DESC", fallback="ssh_from_dc_admins_ips")

    client = boto3.client("ec2")
    security_group = client.describe_security_groups(
        Filters=[{
            "Name": "tag:description",
            "Values": [security_group_desc],
        }]
    )["SecurityGroups"][0]

    ssh_ips = list(filter(
        lambda obj: obj['FromPort'] == 22, 
        security_group["IpPermissions"]
    ))[0]['IpRanges']
    ip_to_remove = list(filter(
        lambda obj: obj["Description"] == description, 
        ssh_ips,
    ))
    if ip_to_remove:
        client.revoke_security_group_ingress(
            GroupId=security_group['GroupId'],
            IpProtocol='tcp',
            FromPort=22,
            ToPort=22,
            CidrIp=ip_to_remove[0]["CidrIp"],
        )

    return client.authorize_security_group_ingress(
        GroupId=security_group["GroupId"],
        IpPermissions=[
            {
                "FromPort": 22,
                "ToPort": 22,
                "IpProtocol": "tcp",
                'IpRanges': [
                    {"CidrIp": f"{ip_to_add}/32", "Description": description},
                ]
            }
        ]
    )
