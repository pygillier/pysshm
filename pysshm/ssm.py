"""SSM client for project"""
import subprocess
import json
import boto3
from loguru import logger
from pick import pick
from pysshm.exception import PySshmException


class Client:
    """Primary SSM client"""

    def __init__(self, profile: str, region: str):
        """__init_ SSM client with correct profile and region"""
        logger.debug("Init with {}/{}", profile, region)

        session = boto3.Session(profile_name=profile, region_name=region)

        self.region = region
        self.profile = profile

        self.client = session.client("ssm")

    def get_available_instances(self) -> str:
        """Returns the list of instances with SSM agent enable in given region"""
        logger.debug("Fetching available instances")

        response = self.client.describe_instance_information()

        instances = [
            (i["ComputerName"], i["InstanceId"], i["IPAddress"], i["PlatformName"])
            for i in response["InstanceInformationList"]
            if i["PingStatus"] == "Online"
        ]
        if len(instances) == 0:
            raise PySshmException(
                f"No instance found in {self.region} region, "
                "are you sure you're in the correct one?"
            )

        title = "Select an instance to connect to:"

        choice = pick(
            instances, title, indicator=">", options_map_func=Client.get_label
        )
        logger.debug("Chosen instance: {}", choice[0][1])

        return choice[0][1]

    @staticmethod
    def get_label(option):
        """Returns a properly formatted label for selection"""
        # pylint: disable=C0209
        return "{:<30} | {:^19} | {:^15} | {:<20} |".format(*option)

    def start_ssh_tunnel(self, config) -> None:
        """Start a SSM session and pass it to session-plugin for real
        connection
        """
        logger.debug("Starting connection to {}", config["Target"])

        session = self.client.start_session(**config)

        del session["ResponseMetadata"]

        cmd = [
            "session-manager-plugin",
            json.dumps(session),
            self.region,
            "StartSession",
            self.profile,
            json.dumps(config),
        ]

        logger.info(session)
        subprocess.run(cmd, check=True)
