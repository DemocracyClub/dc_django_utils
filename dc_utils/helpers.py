import boto3
import getpass
import requests


def add_ip_to_security_group(ip=None, description=None):
    """
    Adds an IP address to the projects SSH admin security groups ingress rules.
    You must have valid AWS credentials configured to run the command. For help
    logging in using SSO see 
    https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html.
    When specifying an IP address to be added, a description must be specified.
    When IP is not specified, defaults to the current public IP address of the
    user running the command. 
    The description defaults to the username of the user running the command.
    """

    if ip and not description:
        raise ValueError(
            "When specifiying an IP to add you must also specify a description"
        )
    
    ip_to_add = ip or requests.get("https://ifconfig.me").text
    description = description or getpass.getuser()

    client = boto3.client("ec2")
    security_group = client.describe_security_groups(
        Filters=[{
            "Name": "tag:description",
            "Values": ["ssh_from_dc_admins_ips"],
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
