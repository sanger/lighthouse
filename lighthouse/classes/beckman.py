import logging
from typing import Dict, List, Optional

from flask import current_app as app

from lighthouse.classes.automation_system import AutomationSystem
from lighthouse.constants.error_messages import ERROR_FAILURE_TYPE_CONFIG, ERROR_ROBOT_CONFIG

logger = logging.getLogger(__name__)


class Beckman(AutomationSystem):
    # Destination plate has been created successfully
    EVENT_DESTINATION_CREATED = "lh_beckman_cp_destination_created"
    # Destination plate failed to be created successfully
    EVENT_DESTINATION_FAILED = "lh_beckman_cp_destination_failed"
    # Source plate only contains negatives, nothing to cherrypick, and the plate is put into the output stacks
    EVENT_SOURCE_ALL_NEGATIVES = "lh_beckman_cp_source_all_negatives"
    # Source plate has had all pickable wells cherrypicked into destination plate(s)
    EVENT_SOURCE_COMPLETED = "lh_beckman_cp_source_completed"
    # Source plate has no related plate map data, cannot be cherrypicked (yet)
    EVENT_SOURCE_NO_PLATE_MAP_DATA = "lh_beckman_cp_source_no_plate_map_data"
    # Source plate barcode cannot be read (damaged or missing), and the plate is put into the output stack
    EVENT_SOURCE_UNRECOGNISED = "lh_beckman_cp_source_plate_unrecognised"

    # needs to be an immutable object: https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables
    PLATE_EVENT_NAMES = (
        EVENT_DESTINATION_CREATED,
        EVENT_DESTINATION_FAILED,
        EVENT_SOURCE_ALL_NEGATIVES,
        EVENT_SOURCE_COMPLETED,
        EVENT_SOURCE_NO_PLATE_MAP_DATA,
        EVENT_SOURCE_UNRECOGNISED,
    )

    def __init__(self) -> None:
        self._name = AutomationSystem.AutomationSystemEnum.BIOSERO.name

    @staticmethod
    def get_robot_uuid(serial_number: str) -> Optional[str]:
        """Maps a robot serial number to a UUID.

        Arguments:
            serial_number (str): The robot serial number.

        Returns:
            Optional[str]: The robot UUID; otherwise None if it cannot be determined.
        """
        uuid = app.config.get("BECKMAN_ROBOTS", {}).get(serial_number, {}).get("uuid", None)

        if uuid is not None:
            return str(uuid)

        return None

    @staticmethod
    def get_robots() -> Optional[List[Dict[str, str]]]:
        logger.debug("Getting Beckman robot information from config...")

        robots_config = app.config.get("BECKMAN_ROBOTS")

        if robots_config is None or not isinstance(robots_config, dict):
            message = "no config found or unreadable"

            logger.error(f"{ERROR_ROBOT_CONFIG} {message}")

            raise Exception(message)

        robots = [{"name": v["name"], "serial_number": k} for k, v in robots_config.items()]

        logger.info("Successfully fetched Beckman robot information")

        return robots

    @staticmethod
    def get_failure_types() -> Optional[List[Dict[str, str]]]:
        logger.debug("Getting Beckman failure types information from config...")

        failure_types_config = app.config.get("BECKMAN_FAILURE_TYPES")

        if failure_types_config is None or not isinstance(failure_types_config, dict):
            message = "no config found or unreadable"

            logger.error(f"{ERROR_FAILURE_TYPE_CONFIG} {message}")

            raise Exception(message)

        failure_types = [{"type": k, "description": v} for k, v in failure_types_config.items()]

        logger.info("Successfully fetched Beckman failure type information")

        return failure_types
