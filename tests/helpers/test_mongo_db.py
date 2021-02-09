from unittest.mock import patch

from lighthouse.constants import (
    FIELD_BARCODE,
    FIELD_DATE_TESTED,
    FIELD_LH_SOURCE_PLATE_UUID,
    FIELD_RESULT,
)
from lighthouse.helpers.mongo_db import get_positive_samples_in_source_plate, get_source_plate_uuid


def test_get_source_plate_uuid_returns_uuid(app, source_plates):
    with app.app_context():
        result = get_source_plate_uuid(source_plates[0][FIELD_BARCODE])
        assert result == source_plates[0][FIELD_LH_SOURCE_PLATE_UUID]


def test_get_source_plate_uuid_returns_none_no_plate_with_barcode(app, source_plates):
    with app.app_context():
        result = get_source_plate_uuid("barcode does not exist")
        assert result is None


def test_get_source_plate_uuid_returns_none_failure_fetching_plates(app, source_plates):
    with app.app_context():
        with patch("flask.current_app.data.driver.db.source_plates") as source_plates_collection:
            source_plates_collection.find_one.side_effect = Exception("Boom!")
            result = get_source_plate_uuid(source_plates[0][FIELD_BARCODE])
            assert result is None


def test_get_positive_samples_in_source_plate_returns_matching_samples(app, samples_with_uuids):
    with app.app_context():
        source_plate_uuid = samples_with_uuids[0][FIELD_LH_SOURCE_PLATE_UUID]
        expected_samples = list(filter(lambda x: x[FIELD_RESULT] == "Positive", samples_with_uuids))
        result = get_positive_samples_in_source_plate(source_plate_uuid)

        # remove the microsecond and tzinfo before comparing
        for res in result:
            res.update(
                {FIELD_DATE_TESTED: res[FIELD_DATE_TESTED].replace(microsecond=0, tzinfo=None)}
            )
        for sample in expected_samples:
            sample.update({FIELD_DATE_TESTED: sample[FIELD_DATE_TESTED].replace(microsecond=0)})

        assert result == expected_samples


def test_get_positive_samples_in_source_plate_returns_empty_list_no_matching_samples(
    app, samples_with_uuids
):
    with app.app_context():
        result = get_positive_samples_in_source_plate("source plate uuid does not exist")
        assert result == []


def test_get_positive_samples_in_source_plate_returns_none_failure_fetching_samples(
    app, samples_with_uuids
):
    with app.app_context():
        with patch("flask.current_app.data.driver.db.samples") as samples_collection:
            samples_collection.find.side_effect = Exception("Boom!")
            result = get_positive_samples_in_source_plate(
                samples_with_uuids[0][FIELD_LH_SOURCE_PLATE_UUID]
            )
            assert result is None
