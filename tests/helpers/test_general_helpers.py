from lighthouse.helpers.general import get_fit_to_pick_samples_and_counts


def test_get_fit_to_pick_samples_count_valid_barcode(app, samples, priority_samples):
    with app.app_context():
        (
            fit_to_pick_samples,
            count_fit_to_pick_samples,
            count_must_sequence,
            count_preferentially_sequence,
            count_filtered_positive,
        ) = get_fit_to_pick_samples_and_counts("plate_123")
        if fit_to_pick_samples:
            assert len(fit_to_pick_samples) == 4
            assert count_fit_to_pick_samples == 4
            assert count_must_sequence == 1
            assert count_preferentially_sequence == 1
            assert count_filtered_positive == 3
        else:
            raise AssertionError()


def test_get_fit_to_pick_samples_count_invalid_barcode(app, samples):
    with app.app_context():
        assert get_fit_to_pick_samples_and_counts("abc") == ([], None, None, None, None)
