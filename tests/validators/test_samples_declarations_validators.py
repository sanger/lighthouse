from lighthouse.validators.samples_declarations import (
    find_duplicates,
    find_non_exist_samples,
    add_flags,
)


def test_find_duplicates():
    assert find_duplicates(["1", "2", "1", "3", "4", "2"]) == ["1", "2"]
    assert find_duplicates([]) == []
    assert find_duplicates(["1", "2", "3", "4"]) == []


def test_find_non_exist_samples(app, samples):
    with app.app_context():
        assert find_non_exist_samples(["MCM001", "MCM003"]) == []
        assert find_non_exist_samples(["MCM004"]) == ["MCM004"]
        assert find_non_exist_samples(["MCM004", "MCM003"]) == ["MCM004"]
        assert find_non_exist_samples(["a", "b", "c"]) == ["a", "b", "c"]


def test_add_flags(app):
    obj = {}
    add_flags(obj, "1234", ["1234"], "TESTING_FLAG")
    assert obj["validation_flags"] == ["TESTING_FLAG"]
    obj = {"validation_flags": ["ANOTHER_VALUE"]}
    add_flags(obj, "1234", ["1234"], "TESTING_FLAG")
    assert obj["validation_flags"] == ["ANOTHER_VALUE", "TESTING_FLAG"]
    obj = {}
    add_flags(obj, "1234", ["4567"], "TESTING_FLAG")
    assert not ("validation_flags" in obj)

