from unittest.mock import patch

from lighthouse.constants.fields import (
    FIELD_DATE_TESTED,
    FIELD_LH_SOURCE_PLATE_UUID,
    FIELD_RESULT,
)
from lighthouse.classes.services.mongo import MongoServiceMixin


def get_positive_samples_in_source_plate(source_plate_uuid):
    mongo_service = MongoServiceMixin()
    result = mongo_service.get_positive_samples_in_source_plate(source_plate_uuid)
    return result


def test_get_positive_samples_in_source_plate_returns_matching_samples(app, samples):
    with app.app_context():
        samples, _ = samples
        source_plate_uuid = samples[0][FIELD_LH_SOURCE_PLATE_UUID]
        expected_samples = list(
            filter(
                lambda x: x[FIELD_RESULT] == "Positive"
                and x.get(FIELD_LH_SOURCE_PLATE_UUID, False) == source_plate_uuid,
                samples,
            )
        )
        result = get_positive_samples_in_source_plate(source_plate_uuid)

        # remove the microsecond before comparing
        if result is not None:
            for res in result:
                res.update({FIELD_DATE_TESTED: res[FIELD_DATE_TESTED].replace(microsecond=0)})
            for sample in expected_samples:
                sample.update({FIELD_DATE_TESTED: sample[FIELD_DATE_TESTED].replace(microsecond=0)})

        assert result == expected_samples


def test_get_positive_samples_in_source_plate_returns_empty_list_no_matching_samples(app, samples):
    with app.app_context():
        result = get_positive_samples_in_source_plate("source plate uuid does not exist")

        assert result == []


def test_get_positive_samples_in_source_plate_returns_none_failure_fetching_samples(app, samples):
    with app.app_context():
        samples, _ = samples
        with patch("flask.current_app.data.driver.db.samples") as samples_collection:
            samples_collection.find.side_effect = Exception()
            result = get_positive_samples_in_source_plate(samples[0][FIELD_LH_SOURCE_PLATE_UUID])

            assert result is None
