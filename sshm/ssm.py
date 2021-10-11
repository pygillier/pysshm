import boto3
import subprocess
import json
from loguru import logger
from pick import pick


class Client:
	

	def __init__(self, profile: str, region: str):
		logger.debug("Init with {}/{}", profile, region)

		session = boto3.Session(
			profile_name=profile,
			region_name=region)

		self.region = region
		self.profile = profile

		self.client = session.client("ssm")

	def get_available_instances(self) -> str:
		"""Returns the list of instances with SSM agent enable in given region"""
		logger.debug("Fetching available instances")

		response = self.client.describe_instance_information()

		instances = [
			(i['ComputerName'], i['InstanceId'], i['IPAddress'], i['PlatformName'])
			for i in response['InstanceInformationList'] if i['PingStatus'] == 'Online'
		]
		title = "Select an instance to connect to:"

		choice = pick(instances, title, indicator='>', options_map_func=Client.get_label)
		logger.debug("Chosen instance: {}", choice[0][1])

		return choice[0][1]


	@staticmethod
	def get_label(option):
		return "{:<30} | {:^19} | {:^15} | {:<20} |".format(*option)


	def start_ssh_tunnel(self, config ) -> None:
		logger.debug("Starting connection to {}", config['Target'])

		session = self.client.start_session(**config)

		del session['ResponseMetadata']

		cmd = [
			'session-manager-plugin',
			json.dumps(session),
			self.region,
			"StartSession",
			self.profile,
			json.dumps(config)
		]

		logger.info(session)
		subprocess.run(
			cmd
		)