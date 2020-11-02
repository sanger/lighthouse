from lighthouse.helpers.dart_db import find_dart_source_samples_rows


def test_get_cherrypicked_samples_from_dart(app, dart_seed_reset):
    with app.app_context():
        found = find_dart_source_samples_rows(app, "test1")
        assert len(found) == 4
        assert found[0].source_barcode == "rna_1"
