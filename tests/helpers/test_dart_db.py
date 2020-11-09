from unittest.mock import patch, Mock
from pytest import raises
from lighthouse.helpers.dart_db import find_dart_source_samples_rows


def test_find_dart_source_samples_rows(app, dart_seed_reset):
    with app.app_context():
        found = find_dart_source_samples_rows(app, "test1")
        assert len(found) == 3
        assert found[0].source_barcode == "123"
        assert found[2].control == "positive"


def test_find_dart_source_samples_rows_not_found_barcode(app, dart_seed_reset):
    with app.app_context():
        found = find_dart_source_samples_rows(app, "unknown")
        assert found == []


def test_exceptions_are_propagated_up(app, dart_seed_reset):
    with app.app_context():
        with patch(
            "lighthouse.helpers.dart_db.create_dart_connection",
            side_effect=Exception("Boom!!"),
        ):
            with raises(Exception):
                found = find_dart_source_samples_rows(app, "unknown")
                assert found is None
