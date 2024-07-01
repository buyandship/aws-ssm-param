import os
import subprocess

import click
DEFAULT_KMS_ALIAS = "alias/app/env"

@click.command()
@click.option("--name", type=str, required=True, help="The name of the parameter (e.g., /myapp/dev/DB_PASSWORD)")
@click.option("--value", type=str, required=True, help="The value of the parameter")
@click.option("--kms-key-id", help="KMS key ID for encryption (example: alias/my-kms-key)")
@click.option("--execute-mode", "-e", is_flag=True, help="Execute mode (perform actual execution)")
def create_secret(name, value, kms_key_id, execute_mode):
    """Upload a single key-value pair to AWS SSM Parameter Store"""
    key_id = kms_key_id or DEFAULT_KMS_ALIAS
    print(f"Using KMS key: {key_id}")

    ssm_app_name = os.getenv("SSM_APP_NAME")
    ssm_env = os.getenv("SSM_ENV")

    if not ssm_app_name or not ssm_env:
        raise ValueError("Both SSM_APP_NAME and SSM_ENV environment variables must be set")
    ssm_path = f"/{ssm_app_name}/{ssm_env}/{name}"

    aws_command = [
        "aws",
        "ssm",
        "put-parameter",
        "--name",
        ssm_path,
        "--value",
        value,
        "--type",
        "SecureString",
        "--overwrite",
        "--key-id",
        key_id,
    ]

    if not execute_mode:
        print(f"Dry run: would upload {ssm_path} to SSM with value {value}")
        return

    try:
        subprocess.run(aws_command, check=True)
        print(f"Successfully uploaded {ssm_path} to SSM")
    except subprocess.CalledProcessError as e:
        print(f"Error uploading {ssm_path} to SSM: {e}")
