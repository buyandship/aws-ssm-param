import click

from aws_ssm_param.create_secret import create_secret
from aws_ssm_param.pull_env_from_source_env import pull_env_from_source_env
from aws_ssm_param.pull_env_from_ssm import pull_env_from_ssm
from aws_ssm_param.upload_env_to_ssm import upload_env_to_ssm

@click.group()
def cli():
    pass

cli.add_command(create_secret)
cli.add_command(pull_env_from_ssm)
cli.add_command(pull_env_from_source_env)
cli.add_command(upload_env_to_ssm)


if __name__ == '__main__':
    cli()