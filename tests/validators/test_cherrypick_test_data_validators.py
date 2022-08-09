from http import HTTPStatus

import pytest

from lighthouse.constants.error_messages import ERROR_PLATE_SPECS_EMPTY_LIST, ERROR_PLATE_SPECS_INVALID_FORMAT


@pytest.mark.parametrize(
    "plate_specs, error_message",
    [
        [[], ERROR_PLATE_SPECS_EMPTY_LIST],
        [["Test"], ERROR_PLATE_SPECS_INVALID_FORMAT],
        [[["Test"]], ERROR_PLATE_SPECS_INVALID_FORMAT],
        [[[1, "Test"]], ERROR_PLATE_SPECS_INVALID_FORMAT],
        [[[1, 2, 3]], ERROR_PLATE_SPECS_INVALID_FORMAT],
        [[[1, 0], "Test"], ERROR_PLATE_SPECS_INVALID_FORMAT],
        [[[1, 0], ["Test"]], ERROR_PLATE_SPECS_INVALID_FORMAT],
        [[[1, 0], [1, "Test"]], ERROR_PLATE_SPECS_INVALID_FORMAT],
        [[[1, 0], [1, 2, 3]], ERROR_PLATE_SPECS_INVALID_FORMAT],
    ],
)
def test_plate_specs_validator_generates_correct_errors(client, plate_specs, error_message):
    response = client.post(
        "/cherrypick-test-data",
        json={"plate_specs": plate_specs},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "plate_specs" in response.json["_issues"]
    assert error_message in response.json["_issues"]["plate_specs"]
