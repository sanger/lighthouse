from http import HTTPStatus

import responses

from lighthouse.helpers.labwhere import get_locations_from_labwhere, set_locations_in_labwhere


def test_get_locations_from_labwhere(app, labwhere_samples_simple):
    with app.app_context():
        response = get_locations_from_labwhere(["plate_123"])

        assert response.json() == [{"barcode": "plate_123", "location_barcode": "location_123"}]


def test_set_locations_in_labwhere(app, mocked_responses):
    with app.app_context():
        labwhere_url = f"http://{app.config['LABWHERE_URL']}/api/scans"
        # The expected payload sent to LabWhere
        payload = {
            "scan": {
                "user_code": "robot-1",
                "labware_barcodes": "123",
                "location_barcode": "location-1-1",
            }
        }
        # The expected response. In practice it's a bit bigger, but I don't think we especially care.
        body = {
            "message": "1 Labwares scanned in to location 1",
            "location": {"name": "Location 1", "barcode": "location-1-1"},
        }

        mocked_responses.add(
            responses.POST,
            labwhere_url,
            match=[responses.json_params_matcher(payload)],
            json=body,
            status=HTTPStatus.OK,
        )

        response = set_locations_in_labwhere(["123"], "location-1-1", "robot-1")

        assert response
