from flask import current_app as app
from lighthouse.constants.fields import FIELD_BARCODE, FIELD_LH_SOURCE_PLATE_UUID, FIELD_LH_SAMPLE_UUID, FIELD_PLATE_BARCODE


class ServiceMongoMixin:
    def get_samples_from_mongo(self, uuids):
        samples_collection = app.data.driver.db.samples  # type: ignore

        samples = list(samples_collection.find({FIELD_LH_SAMPLE_UUID: {"$in": uuids}}))

        obtained_uuids = [sample[FIELD_LH_SAMPLE_UUID] for sample in samples]

        remaining_uuids = list(set(uuids) - set(obtained_uuids))

        if len(remaining_uuids) > 0:
            raise Exception(
                f"Some samples cannot be obtained because are not present in Mongo. Please review: {remaining_uuids}"
            )
        return samples

    def get_source_plate_uuid(self, barcode):
        with app.app_context():
            source_plates_collection = app.data.driver.db.source_plates  # type: ignore

            plate = source_plates_collection.find_one({FIELD_BARCODE: barcode})
            if plate is None:
                raise Exception(f"Source plate with barcode {barcode} not found")
            return plate[FIELD_LH_SOURCE_PLATE_UUID]

    def get_samples_from_mongo_for_barcode(self, barcode):
        samples_collection = app.data.driver.db.samples  # type: ignore

        samples = list(samples_collection.find({FIELD_PLATE_BARCODE: barcode}))

        return samples
