from flask import current_app as app
from lighthouse.helpers.labwhere import set_locations_in_labwhere
from typing import Any


class LabwhereServiceMixin:
    def transfer_to_bin(self: Any) -> None:
        """Record a transfer of the cherrypicking_source_labware to the bin

        Args:
            event (Message): The event for which to fire a callback

        Returns:
            Tuple[bool, List[str]]: True if the operation completed successfully; any errors attempting to construct the
            message, otherwise an empty array.
        """
        # currently assuming only one event so only one plate_barcode
        labware_barcodes = [self.properties["plate_barcode"].value]
        location_barcode = LabwhereServiceMixin._destroyed_barcode()
        robot_barcode = self.properties["automation_system_name"].value

        response = set_locations_in_labwhere(
            labware_barcodes=labware_barcodes,
            location_barcode=location_barcode,
            user_barcode=robot_barcode,
        )
        if not response.ok:
            raise Exception(
                f"There was some problem when sending changing location in labwhere: { response.text }"
            )


    @staticmethod
    def _destroyed_barcode() -> str:
        """The barcode associated with the destroyed labware location in LabWhere.

        As this value can vary between environments, it is part of the app context and is configured in
        `config/defaults.py` or the appropriate environment file. You can also specify the barcode in the
        `LABWHERE_DESTROYED_BARCODE` environmental variable, which is useful in development mode.

        Returns:
            str: barcode associated with the destroyed labware location in LabWhere
        """
        return str(app.config["LABWHERE_DESTROYED_BARCODE"])
