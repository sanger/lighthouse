import logging
from typing import cast

from eve import Eve
from flask import current_app as app

from lighthouse.constants.fields import (
    FIELD_BARCODE,
    FIELD_LH_SAMPLE_UUID,
    FIELD_LH_SOURCE_PLATE_UUID,
    FIELD_PLATE_BARCODE,
)

logger = logging.getLogger(__name__)


class MongoServiceMixin:
    def get_samples_from_mongo(self, uuids):
        logger.debug("> get_samples_from_mongo")
        if len(uuids) == 0:
            return []

        samples_collection = cast(Eve, app).data.driver.db.samples

        samples = list(samples_collection.find({FIELD_LH_SAMPLE_UUID: {"$in": uuids}}))

        obtained_uuids = [sample[FIELD_LH_SAMPLE_UUID] for sample in samples]

        remaining_uuids = list(set(uuids) - set(obtained_uuids))

        if len(remaining_uuids) > 0:
            raise Exception(
                (
                    "Some samples cannot be obtained because they are not "
                    f"present in Mongo. Please review: {remaining_uuids}"
                )
            )
        return samples

    def get_source_plate_uuid(self, barcode):
        with app.app_context():
            source_plates_collection = cast(Eve, app).data.driver.db.source_plates

            plate = source_plates_collection.find_one({FIELD_BARCODE: barcode})
            if plate is None:
                raise Exception(f"Source plate with barcode '{barcode}' not found")
            return plate[FIELD_LH_SOURCE_PLATE_UUID]

    def get_samples_from_mongo_for_barcode(self, barcode):
        samples_collection = cast(Eve, app).data.driver.db.samples

        samples = list(samples_collection.find({FIELD_PLATE_BARCODE: barcode}))

        return samples

    def get_source_plates_from_barcodes(self, barcodes):
        with app.app_context():
            source_plates_collection = cast(Eve, app).data.driver.db.source_plates

            source_plates = list(source_plates_collection.find({FIELD_BARCODE: {"$in": barcodes}}))

            obtained_barcodes = [source_plate[FIELD_BARCODE] for source_plate in source_plates]

            remaining_barcodes = list(set(barcodes) - set(obtained_barcodes))

            if len(remaining_barcodes) > 0:
                raise Exception(
                    (
                        "Some source plate barcodes cannot be obtained because are not present in Mongo. "
                        f"Please review: {remaining_barcodes}"
                    )
                )

            return source_plates
