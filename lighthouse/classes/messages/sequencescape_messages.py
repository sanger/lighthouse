from flask import current_app as app
from lighthouse.messages.message import Message
from typing import Dict
import requests
import logging

logger = logging.getLogger(__name__)


class SequencescapeMessage(Message):
    def __init__(self):
        self._barcode = None
        self._contents = {}

    def set_barcode(self, barcode):
        self._barcode = barcode

    def set_well_sample(self, location, sample_info):
        self._contents[location] = sample_info

    def render(self) -> Message:
        message_content = self.construct_sequencescape_message(
            barcode=self._barcode,
            purpose_uuid=app.config["SS_UUID_PLATE_PURPOSE_CHERRYPICKED"],
            study_uuid=app.config["SS_UUID_STUDY_CHERRYPICKED"],
            wells=self._contents,
            events=[],
        )

        return Message(message_content)

    def construct_sequencescape_message(self, barcode, purpose_uuid, study_uuid, wells, events):
        body = {
            "barcode": barcode,
            "purpose_uuid": purpose_uuid,
            "study_uuid": study_uuid,
            "wells": wells,
            "events": events,
        }

        return {"data": {"type": "plates", "attributes": body}}

    def send_to_ss(self):
        message = self.render()
        return self._send_to_ss(
            ss_url=app.config["SS_PLATE_CREATION_ENDPOINT"],
            headers={"X-Sequencescape-Client-Id": app.config["SS_API_KEY"], "Content-type": "application/json"},
            data=message.payload(),
        )

    def _send_to_ss(self, ss_url: str, headers: Dict[str, str], data: str) -> requests.Response:
        """Send JSON body to the Sequencescape /heron/plates endpoint. This should create the plate in Sequencescape.

        Arguments:
            body (Dict[str, Any]): the info of the plate to create in Sequencescape.

        Raises:
            requests.ConnectionError: if a connection to Sequencescape is not able to be made.

        Returns:
            requests.Response: the response from Sequencescape.
        """

        logger.info(f"Sending request to: {ss_url}")

        try:
            response = requests.post(ss_url, data=data, headers=headers)

            logger.debug(f"Response status code: {response.status_code}")

            return response
        except requests.ConnectionError:
            raise requests.ConnectionError("Unable to access Sequencescape")
