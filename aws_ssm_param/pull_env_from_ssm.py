import os
import subprocess
import click


def pull_env_from_ssm_impl(ssm_app_name, ssm_env) -> str:
    print(f'Pulling environment from SSM for app: {ssm_app_name} and env: {ssm_env}')
    ssm_path_prefix = f"/{ssm_app_name}/{ssm_env}"

    # Execute AWS SSM command and handle output redirection
    aws_command = [
        "aws",
        "ssm",
        "get-parameters-by-path",
        "--path",
        ssm_path_prefix,
        "--with-decryption",
        "--query",
        "Parameters[*].[Name,Value]",
        "--output",
        "text",
    ]
    try:
        aws_process = subprocess.run(aws_command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        print(f"Standard Error: {e.stderr}")
        raise

    output = ""
    for line in aws_process.stdout.split("\n"):
        if not line:
            continue
        line = line.strip()
        name, value = line.split("\t", 1)
        name = name.replace(f"{ssm_path_prefix}/", "")
        output += f"{name}={value}\n"
    return output

@click.command()
@click.option("--output-file", "-o", help="Output file (optional)")
def pull_env_from_ssm(output_file):
    """Execute AWS SSM command and handle output redirection"""

    # Retrieve SSM_APP_NAME and SSM_ENV from environment variables
    ssm_app_name = os.getenv('SSM_APP_NAME')
    ssm_env = os.getenv('SSM_ENV')

    if not ssm_app_name or not ssm_env:
        raise ValueError("Both SSM_APP_NAME and SSM_ENV environment variables must be set")

    # Redirect output to file if OUTPUT_FILE is specified, otherwise to console
    if output_file:
        with open(output_file, "w") as f:
            f.write(pull_env_from_ssm_impl(ssm_app_name, ssm_env))
    else:
        print(pull_env_from_ssm_impl(ssm_app_name, ssm_env))

