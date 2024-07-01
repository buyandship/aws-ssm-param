#!/usr/bin/env python3

import os
import click

from .pull_env_from_ssm import pull_env_from_ssm_impl


def load_env(file):
    env = {}
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env[key] = value
    return env


def load_env_from_str(env_str):
    env = {}
    for line in env_str.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            key, value = line.split('=', 1)
            env[key] = value
    return env


def merge_envs(env1, env2):
    merged_env = env1.copy()
    for key, value in env2.items():
        if key in merged_env:
            merged_env[key] = value
    return merged_env


def write_to_file(env, output_file):
    with open(output_file, 'w') as f:
        for key, value in env.items():
            f.write(f'{key}={value}\n')


@click.command()
@click.option('--source-env', type=str, help='Path to the source environment file')
@click.option('--output', '-o', type=str, help='Path to the output file')
def pull_env_from_source_env(source_env, output):
    """Update source key values with remote key values"""
    env_source_file = source_env

    ssm_app_name = os.getenv('SSM_APP_NAME')
    ssm_env = os.getenv('SSM_ENV')

    if not ssm_app_name or not ssm_env:
        raise ValueError('Both SSM_APP_NAME and SSM_ENV environment variables must be set')

    remote_env_str = pull_env_from_ssm_impl(ssm_app_name, ssm_env)

    env_source = load_env(env_source_file)
    env_remote = load_env_from_str(remote_env_str)

    merged_env = merge_envs(env_source, env_remote)

    if output:
        write_to_file(merged_env, output)
    else:
        for key, value in merged_env.items():
            print(f'{key}={value}')
