#!/usr/bin/env python3
from setuptools import setup

setup(
    install_requires=[
        "boto3", "requests"
    ],
    entry_points = {
        "console_scripts": [
            "add_ip_to_sg=dc_utils.helpers.update_ec2_sg.utils:add_ip_to_security_group",
            "remove_ip_from_sg=dc_utils.helpers.update_ec2_sg.utils:remove_ip_from_security_group",
        ]
    }
)
