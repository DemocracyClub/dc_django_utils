#!/usr/bin/env python3
from importlib.metadata import entry_points
import json
import os

from setuptools import setup

setup(
    entry_points = {
        "console_scripts": ["add_ip_to_sg=helpers.update_ec2_sg.add_ip.add_ip_to_security_group"]
    }
)
