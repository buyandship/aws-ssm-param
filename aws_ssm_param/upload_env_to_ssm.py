import os

import click

from aws_ssm_param.create_secret import put_parameter

DEFAULT_KMS_ALIAS = "alias/app/env"

@click.command()
@click.option("--env-file", "-f", required=True, help="Environment file")
@click.option("--kms-key-id", "-k", help="KMS key ID for encryption (example: alias/my-kms-key)")
@click.option("--type", "-t", "value_type", help="Type of parameter (String, StringList, SecureString)")
@click.option("--execute-mode", "-e", is_flag=True, help="Execute mode (perform actual execution)")
def upload_env_to_ssm(env_file, kms_key_id, value_type, execute_mode):
    """Store environment variables in AWS SSM"""
    ssm_app_name = os.getenv('SSM_APP_NAME')
    ssm_env = os.getenv('SSM_ENV')

    if not ssm_app_name or not ssm_env:
        raise ValueError("Both SSM_APP_NAME and SSM_ENV environment variables must be set")

    kms_key_id = kms_key_id or DEFAULT_KMS_ALIAS
    value_type = value_type or "String"

    print(f"Using KMS key: {kms_key_id}")
    print(f"Using value type: {value_type}")

    if not os.path.isfile(env_file):
        print("File not found:", env_file)
        exit(1)

    with open(env_file, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("#") or not line:
                continue

            var_name, var_value = line.split("=", 1)
            ssm_path = f"/{ssm_app_name}/{ssm_env}/{var_name}"

            put_parameter(ssm_path, var_value, value_type, kms_key_id, execute_mode)