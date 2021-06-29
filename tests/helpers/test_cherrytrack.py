from http import HTTPStatus

import responses

from lighthouse.helpers.cherrytrack import (
    get_automation_system_run_info_from_cherrytrack,
    get_samples_from_source_plate_barcode_from_cherrytrack,
    get_wells_from_destination_barcode_from_cherrytrack,
)

from tests.fixtures.data.biosero.automation_system_runs import RUNS
from tests.fixtures.data.biosero.source_plate_wells import SOURCE_PLATE_WELLS
from tests.fixtures.data.biosero.destination_plate_wells import DESTINATION_PLATE_WELLS


def test_get_automation_system_run_info_from_cherrytrack(app, mocked_responses):
    with app.app_context():
        run = RUNS[0]

        cherrytrack_url = f"{app.config['CHERRYTRACK_URL']}/automation-system-runs/{run['id']}"

        body = {"data": run}
        mocked_responses.add(responses.GET, cherrytrack_url, json=body, status=HTTPStatus.CREATED)

        response = get_automation_system_run_info_from_cherrytrack(run["id"])
        assert response.status_code == HTTPStatus.CREATED

        assert response.json() == body


def test_get_samples_from_source_plate_barcode_from_cherrytrack(app, mocked_responses):
    with app.app_context():
        source_plate_barcode = "DS000010003"
        cherrytrack_url = f"{app.config['CHERRYTRACK_URL']}/source-plates/{source_plate_barcode}"
        body = {"data": {"samples": SOURCE_PLATE_WELLS}}
        mocked_responses.add(responses.GET, cherrytrack_url, json=body, status=HTTPStatus.CREATED)

        response = get_samples_from_source_plate_barcode_from_cherrytrack(source_plate_barcode)
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == body


def test_get_wells_from_destination_barcode_from_cherrytrack(app, mocked_responses):
    with app.app_context():
        destination_plate_barcode = "DN00000001"

        cherrytrack_url = f"{app.config['CHERRYTRACK_URL']}/destination-plates/{destination_plate_barcode}"

        body = {"data": {"wells": DESTINATION_PLATE_WELLS}}
        mocked_responses.add(responses.GET, cherrytrack_url, json=body, status=HTTPStatus.CREATED)

        response = get_wells_from_destination_barcode_from_cherrytrack(destination_plate_barcode)
        assert response.status_code == HTTPStatus.CREATED

        assert response.json() == body
