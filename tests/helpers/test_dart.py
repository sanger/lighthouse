from unittest.mock import patch

from pytest import raises

from lighthouse.constants.fields import FIELD_DART_CONTROL, FIELD_DART_SOURCE_BARCODE
from lighthouse.helpers.dart import find_dart_source_samples_rows


def test_find_dart_source_samples_rows(app, dart_samples):
    with app.app_context():
        found = find_dart_source_samples_rows("des_plate_1")
        print(found)
        assert len(found) == 6
        assert getattr(found[0], FIELD_DART_SOURCE_BARCODE) == "plate_123"
        assert getattr(found[4], FIELD_DART_CONTROL) == "positive"


def test_find_dart_source_samples_rows_not_found_barcode(app, dart_samples):
    with app.app_context():
        found = find_dart_source_samples_rows("unknown")
        assert found == []


def test_exceptions_are_propagated_up(app, dart_samples):
    with app.app_context():
        with patch("lighthouse.db.dart.create_dart_connection", side_effect=Exception()):
            found = find_dart_source_samples_rows("unknown")
            with raises(Exception):
                found = find_dart_source_samples_rows("unknown")
                assert found is None
