from unittest.mock import patch

from lighthouse.constants import FIELD_DART_CONTROL, FIELD_DART_SOURCE_BARCODE
from lighthouse.helpers.dart_db import find_dart_source_samples_rows
from pytest import raises


def test_find_dart_source_samples_rows(app, dart_seed_reset):
    with app.app_context():
        found = find_dart_source_samples_rows("test1")
        assert len(found) == 3
        assert getattr(found[0], FIELD_DART_SOURCE_BARCODE) == "123"
        assert getattr(found[2], FIELD_DART_CONTROL) == "positive"


def test_find_dart_source_samples_rows_not_found_barcode(app, dart_seed_reset):
    with app.app_context():
        found = find_dart_source_samples_rows("unknown")
        assert found == []


def test_exceptions_are_propagated_up(app, dart_seed_reset):
    with app.app_context():
        with patch(
            "lighthouse.helpers.dart_db.create_dart_connection", side_effect=Exception("Boom!!"),
        ):
            with raises(Exception):
                found = find_dart_source_samples_rows("unknown")
                assert found is None
