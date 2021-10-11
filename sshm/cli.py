import click
from loguru import logger
from .ssm import Client
from . import log


@click.command()
@click.option("-p", "--profile", default="default", envvar="AWS_PROFILE", help="AWS profile")
@click.option("-r", "--region", default="eu-west-3", envvar="AWS_REGION", help="AWS region (default: eu-west-3)")
@click.option("-i", "--instance-id", default=None, help="Instance ID for direct connect")
@click.option("-d", "--debug", is_flag=True, default=False, help="Enable debug")
def run(profile: str, region: str, instance_id: str, debug: bool) -> None:
	"""Connect to an EC2 instance over SSM, all in your favorite shell."""

	log.configure(debug=debug)

	ssm_client = Client(profile=profile, region=region)

	if instance_id is None:
		# No instance provided, offer the list
		instance_id = ssm_client.get_available_instances()

	# Port forward, someday
	tunnel_config = {
		'Target': instance_id
	}


	# Init the real connection
	ssm_client.start_ssh_tunnel(tunnel_config)