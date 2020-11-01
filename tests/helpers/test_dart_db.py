from lighthouse.helpers.dart_db import find_dart_source_samples_rows


def test_get_cherrypicked_samples_from_dart(app, dart_seed_reset):
    with app.app_context():
        found = find_dart_source_samples_rows(app, "TARGET1234")
        assert len(found) == 3
        assert found[0].source_barcode == "SOURCE1234"
