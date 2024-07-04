import os
import subprocess

import click
import json

DEFAULT_KMS_ALIAS = "alias/app/env"

@click.command()
@click.option("--env-file", "-f", required=True, help="Environment file")
@click.option("--kms-key-id", "-k", help="KMS key ID for encryption (example: alias/my-kms-key)")
@click.option("--execute-mode", "-e", is_flag=True, help="Execute mode (perform actual execution)")
def upload_env_to_ssm(env_file, kms_key_id, execute_mode):
    """Store environment variables in AWS SSM"""
    ssm_app_name = os.getenv('SSM_APP_NAME')
    ssm_env = os.getenv('SSM_ENV')

    if not ssm_app_name or not ssm_env:
        raise ValueError("Both SSM_APP_NAME and SSM_ENV environment variables must be set")

    kms_key_id = kms_key_id or DEFAULT_KMS_ALIAS
    print(f"Using KMS key: {kms_key_id}")

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
            json_dict = {
                "Type": "SecureString",
                "Name": ssm_path,
                "Value": var_value,
            }

            if not execute_mode:
                print(f"Dry run: would put {var_name} to {ssm_path} with value {var_value}")
            else:
                command = [
                    "aws",
                    "ssm",
                    "put-parameter",
                    "--cli-input-json",
                    json.dumps(json_dict),
                    "--overwrite",
                    "--key-id",
                    kms_key_id,
                ]
                result = subprocess.run(command)
                if result.returncode == 0:
                    print(f"Successfully put {var_name} to {ssm_path}")
                else:
                    print(f"Failed to put {var_name} to {ssm_path}")

