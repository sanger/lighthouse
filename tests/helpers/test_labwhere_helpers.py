from lighthouse.helpers.labwhere import get_locations_from_labwhere, set_locations_in_labwhere
import responses  # type: ignore
from http import HTTPStatus
import json


def test_get_locations_from_labwhere(app, labwhere_samples_simple):
    with app.app_context():
        response = get_locations_from_labwhere("123")
        assert response.json() == [{"barcode": "123", "location_barcode": "4567"}]


