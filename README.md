# pysshm

Connect to a SSM session directly in your favorite terminal.

## Install

In your terminal, run:

```bash
$ pip install pysshm
```

In order to fully use pysshm, you **MUST** install the [session-manager-plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html) from AWS.

## Usage

```bash
$ pysshm --help
Usage: pysshm [OPTIONS]

  Connect to an EC2 instance over SSM, all in your favorite shell.

Options:
  -p, --profile TEXT      AWS profile
  -r, --region TEXT       AWS region (default: eu-west-3)
  -i, --instance-id TEXT  Instance ID for direct connect
  -d, --debug             Enable debug
  --help                  Show this message and exit.
```
