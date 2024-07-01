# Install
```
pip install git+https://github.com/buyandship/aws-ssm-param.git
```

# Usage
You need aws profile to run following command.

export `SSM_APP_NAME` and `SSM_ENV` to use script
### Example
```sh
export SSM_APP_NAME=your_service_name
export SSM_ENV=staging # dev/staging/production
```

## Pull secret from ssm
```bash
aws-ssm-param pull_env_from_ssm -o $output.env
```

## Generate env from source env as keys and merge with ssm parameters
### Example

.env.source
```
a=123
b=345
c=
```

remote (ssm)
```
a=777
b=999
d=should_not_include
```

```sh
aws-ssm-param pull_env_from_source_env {.env} -o $output.env
```

will result
```
a=777
b=999
c=
```

## Upload whole env file to ssm
```sh
aws-ssm-param upload_env_to_ssm -f ${env_file}

# real execution
aws-ssm-param upload_env_to_ssm -f ${env_file} -e
```

## Upload single key value to ssm
```sh
aws-ssm-param create_secret ${name} ${value}
# real execution
aws-ssm-param create_secret ${name} ${value} -e
```
