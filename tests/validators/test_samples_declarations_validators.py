from lighthouse.validators.samples_declarations import (
    find_duplicates,
    find_non_exist_samples,
    add_flags,
    build_clean_elems_object,
    merge_response_into_payload,
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
        assert sorted(find_non_exist_samples(["a", "b", "c"])) == sorted(["a", "b", "c"])


def test_add_flags(app):
    obj = {"root_sample_id": "1234"}
    add_flags(obj, ["1234"], "TESTING_FLAG")
    assert obj["validation_flags"] == ["TESTING_FLAG"]

    obj = {"validation_flags": ["ANOTHER_VALUE"], "root_sample_id": "1234"}
    add_flags(obj, "1234", "TESTING_FLAG")
    assert obj["validation_flags"] == ["ANOTHER_VALUE", "TESTING_FLAG"]

    obj = {"root_sample_id": "1234"}
    add_flags(obj, ["4567"], "TESTING_FLAG")
    assert not ("validation_flags" in obj)


def test_build_clean_elems_object(app):
    class TestRequest:
        def __init__(self):
            self.json = ["a", "b", "c"]

    assert build_clean_elems_object([], TestRequest()) == {}

    assert build_clean_elems_object(
        [{"_status": "OK"}, {"_status": "ERR"}, {"_status": "OK"}], TestRequest()
    ) == {0: "a", 2: "c"}

    assert build_clean_elems_object(
        [{"_status": "ERR"}, {"_status": "OK"}, {"_status": "ERR"}], TestRequest()
    ) == {1: "b"}


def test_merge_response_into_payload():
    class TestPayload:
        def __init__(self, json):
            self.json = json

    payload = TestPayload({"_items": ["good response 1", "bad response 2", "good response 3"]})
    response = {"_items": ["good response A", "good response B"]}
    clean_elems = {0: "good response 1", 2: "good response 2"}

    assert merge_response_into_payload(payload, response, clean_elems).json == {
        "_items": ["good response A", "bad response 2", "good response B"]
    }
