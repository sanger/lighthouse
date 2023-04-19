# import urllib.parse
# from http import HTTPStatus
# from unittest.mock import patch

import pytest
import responses

# from lighthouse.constants.general import ARG_EXCLUDE, ARG_TYPE, ARG_TYPE_DESTINATION, ARG_TYPE_SOURCE

ENDPOINT_PREFIXES = ["", "/v1"]
GET_PICKINGS_ENDPOINT = "/pickings"

GET_PICKINGS_ENDPOINTS = [prefix + GET_PICKINGS_ENDPOINT for prefix in ENDPOINT_PREFIXES]


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
def test_get_pickings_endpoint_success(app, client, mocked_responses, endpoint):
    barcode = "ABCD-1234"
    ss_url = (
        f"{app.config['SS_URL']}/api/v2/labware?filter[barcode]={barcode}&include=purpose,receptacles.aliquots.sample"
    )

    body = {
        "data": [
            {
                "id": "17",
                "type": "plates",
                "links": {"self": "http://127.0.0.1:3000/api/v2/plates/17"},
                "attributes": {
                    "uuid": "89fc5d50-d9fd-11ed-9d29-acde48001122",
                    "name": "Plate SQPD-9014",
                    "labware_barcode": {
                        "ean13_barcode": null,
                        "machine_barcode": "SQPD-9014",
                        "human_barcode": "SQPD-9014",
                    },
                    "state": "pending",
                    "created_at": "2023-04-13T14:17:28+01:00",
                    "updated_at": "2023-04-13T14:17:28+01:00",
                    "number_of_rows": 8,
                    "number_of_columns": 12,
                    "size": 96,
                },
                "relationships": {},
            }
        ],
        "included": [
            {
                "id": "57",
                "type": "purposes",
                "links": {"self": "http://127.0.0.1:3000/api/v2/purposes/57"},
                "attributes": {
                    "uuid": "a0bb754c-d487-11ed-9025-acde48001122",
                    "name": "LBSN-96 Lysate",
                    "size": 96,
                    "lifespan": null,
                },
            },
            {
                "id": "2692",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2692"},
                "attributes": {
                    "uuid": "8cd51db4-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:A1",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "A1"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/aliquots",
                        },
                        "data": [{"type": "aliquots", "id": "123"}],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2692/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2692/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2693",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2693"},
                "attributes": {
                    "uuid": "8cf49f04-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:B1",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "B1"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/aliquots",
                        },
                        "data": [{"type": "aliquots", "id": "124"}],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2693/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2693/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2694",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2694"},
                "attributes": {
                    "uuid": "8cf6b9ba-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:C1",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "C1"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/aliquots",
                        },
                        "data": [{"type": "aliquots", "id": "125"}],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2694/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2694/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2695",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2695"},
                "attributes": {
                    "uuid": "8d0041e2-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:D1",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "D1"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/aliquots",
                        },
                        "data": [{"type": "aliquots", "id": "126"}],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2695/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2695/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2696",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2696"},
                "attributes": {
                    "uuid": "8d0299d8-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:E1",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "E1"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2696/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2696/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2697",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2697"},
                "attributes": {
                    "uuid": "8d0498fa-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:F1",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "F1"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2697/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2697/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2698",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2698"},
                "attributes": {
                    "uuid": "8d063e26-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:G1",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "G1"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2698/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2698/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2699",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2699"},
                "attributes": {
                    "uuid": "8d07e2f8-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:H1",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "H1"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2699/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2699/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2700",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2700"},
                "attributes": {
                    "uuid": "8d098964-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:A2",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "A2"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2700/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2700/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2701",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2701"},
                "attributes": {
                    "uuid": "8d0b8a8e-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:B2",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "B2"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2701/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2701/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2702",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2702"},
                "attributes": {
                    "uuid": "8d0da59e-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:C2",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "C2"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2702/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2702/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2703",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2703"},
                "attributes": {
                    "uuid": "8d0fd288-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:D2",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "D2"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2703/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2703/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2704",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2704"},
                "attributes": {
                    "uuid": "8d12143a-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:E2",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "E2"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2704/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2704/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2705",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2705"},
                "attributes": {
                    "uuid": "8d1411d6-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:F2",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "F2"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2705/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2705/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2706",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2706"},
                "attributes": {
                    "uuid": "8d1612a6-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:G2",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "G2"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2706/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2706/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2707",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2707"},
                "attributes": {
                    "uuid": "8d18553e-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:H2",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "H2"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2707/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2707/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2708",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2708"},
                "attributes": {
                    "uuid": "8d1d43f0-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:A3",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "A3"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2708/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2708/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2709",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2709"},
                "attributes": {
                    "uuid": "8d1f5500-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:B3",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "B3"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2709/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2709/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2710",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2710"},
                "attributes": {
                    "uuid": "8d21ce02-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:C3",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "C3"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2710/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2710/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2711",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2711"},
                "attributes": {
                    "uuid": "8d23588a-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:D3",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "D3"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2711/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2711/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2712",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2712"},
                "attributes": {
                    "uuid": "8d2567ba-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:E3",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "E3"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2712/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2712/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2713",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2713"},
                "attributes": {
                    "uuid": "8d274c24-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:F3",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "F3"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2713/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2713/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2714",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2714"},
                "attributes": {
                    "uuid": "8d296702-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:G3",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "G3"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2714/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2714/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2715",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2715"},
                "attributes": {
                    "uuid": "8d2b4dec-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:H3",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "H3"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2715/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2715/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2716",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2716"},
                "attributes": {
                    "uuid": "8d2d0fce-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:A4",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "A4"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2716/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2716/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2717",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2717"},
                "attributes": {
                    "uuid": "8d2eb2fc-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:B4",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "B4"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2717/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2717/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2718",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2718"},
                "attributes": {
                    "uuid": "8d3063ae-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:C4",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "C4"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2718/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2718/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2719",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2719"},
                "attributes": {
                    "uuid": "8d32461a-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:D4",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "D4"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2719/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2719/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2720",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2720"},
                "attributes": {
                    "uuid": "8d344e9c-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:E4",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "E4"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2720/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2720/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2721",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2721"},
                "attributes": {
                    "uuid": "8d373bd4-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:F4",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "F4"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2721/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2721/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2722",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2722"},
                "attributes": {
                    "uuid": "8d38da52-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:G4",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "G4"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2722/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2722/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2723",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2723"},
                "attributes": {
                    "uuid": "8d3a7330-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:H4",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "H4"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2723/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2723/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2724",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2724"},
                "attributes": {
                    "uuid": "8d3bfdae-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:A5",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "A5"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2724/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2724/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2725",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2725"},
                "attributes": {
                    "uuid": "8d3d9a7e-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:B5",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "B5"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2725/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2725/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2726",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2726"},
                "attributes": {
                    "uuid": "8d3f67d2-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:C5",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "C5"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2726/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2726/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2727",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2727"},
                "attributes": {
                    "uuid": "8d412798-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:D5",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "D5"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2727/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2727/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2728",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2728"},
                "attributes": {
                    "uuid": "8d42f5be-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:E5",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "E5"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2728/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2728/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2729",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2729"},
                "attributes": {
                    "uuid": "8d44a6de-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:F5",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "F5"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2729/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2729/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2730",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2730"},
                "attributes": {
                    "uuid": "8d467450-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:G5",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "G5"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2730/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2730/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2731",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2731"},
                "attributes": {
                    "uuid": "8d4842c6-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:H5",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "H5"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2731/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2731/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2732",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2732"},
                "attributes": {
                    "uuid": "8d499996-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:A6",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "A6"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2732/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2732/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2733",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2733"},
                "attributes": {
                    "uuid": "8d4b7d24-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:B6",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "B6"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2733/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2733/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2734",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2734"},
                "attributes": {
                    "uuid": "8d4d667a-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:C6",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "C6"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2734/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2734/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2735",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2735"},
                "attributes": {
                    "uuid": "8d4ee784-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:D6",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "D6"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2735/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2735/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2736",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2736"},
                "attributes": {
                    "uuid": "8d505c04-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:E6",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "E6"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2736/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2736/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2737",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2737"},
                "attributes": {
                    "uuid": "8d51ebfa-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:F6",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "F6"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2737/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2737/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2738",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2738"},
                "attributes": {
                    "uuid": "8d5475d2-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:G6",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "G6"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2738/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2738/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2739",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2739"},
                "attributes": {
                    "uuid": "8d563aca-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:H6",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "H6"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2739/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2739/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2740",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2740"},
                "attributes": {
                    "uuid": "8d5800ee-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:A7",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "A7"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2740/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2740/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2741",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2741"},
                "attributes": {
                    "uuid": "8d59f2aa-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:B7",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "B7"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2741/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2741/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2742",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2742"},
                "attributes": {
                    "uuid": "8d5bbd10-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:C7",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "C7"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2742/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2742/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2743",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2743"},
                "attributes": {
                    "uuid": "8d5d62e6-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:D7",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "D7"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2743/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2743/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2744",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2744"},
                "attributes": {
                    "uuid": "8d5f57a4-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:E7",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "E7"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2744/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2744/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2745",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2745"},
                "attributes": {
                    "uuid": "8d61390c-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:F7",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "F7"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2745/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2745/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2746",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2746"},
                "attributes": {
                    "uuid": "8d64671c-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:G7",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "G7"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2746/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2746/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2747",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2747"},
                "attributes": {
                    "uuid": "8d65f47e-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:H7",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "H7"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2747/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2747/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2748",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2748"},
                "attributes": {
                    "uuid": "8d677bb4-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:A8",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "A8"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2748/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2748/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2749",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2749"},
                "attributes": {
                    "uuid": "8d692392-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:B8",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "B8"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2749/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2749/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2750",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2750"},
                "attributes": {
                    "uuid": "8d6acad0-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:C8",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "C8"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2750/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2750/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2751",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2751"},
                "attributes": {
                    "uuid": "8d6c851e-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:D8",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "D8"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2751/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2751/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2752",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2752"},
                "attributes": {
                    "uuid": "8d6e2ad6-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:E8",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "E8"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2752/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2752/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2753",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2753"},
                "attributes": {
                    "uuid": "8d6fbc70-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:F8",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "F8"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2753/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2753/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2754",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2754"},
                "attributes": {
                    "uuid": "8d7aeb90-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:G8",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "G8"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2754/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2754/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2755",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2755"},
                "attributes": {
                    "uuid": "8d81f552-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:H8",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "H8"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2755/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2755/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2756",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2756"},
                "attributes": {
                    "uuid": "8d83cb0c-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:A9",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "A9"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2756/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2756/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2757",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2757"},
                "attributes": {
                    "uuid": "8d85be62-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:B9",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "B9"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2757/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2757/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2758",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2758"},
                "attributes": {
                    "uuid": "8d878044-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:C9",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "C9"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2758/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2758/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2759",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2759"},
                "attributes": {
                    "uuid": "8d89117a-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:D9",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "D9"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2759/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2759/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2760",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2760"},
                "attributes": {
                    "uuid": "8d8abbe2-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:E9",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "E9"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2760/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2760/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2761",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2761"},
                "attributes": {
                    "uuid": "8d8c714e-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:F9",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "F9"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2761/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2761/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2762",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2762"},
                "attributes": {
                    "uuid": "8d8e6a8a-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:G9",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "G9"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2762/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2762/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2763",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2763"},
                "attributes": {
                    "uuid": "8d910772-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:H9",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "H9"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2763/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2763/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2764",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2764"},
                "attributes": {
                    "uuid": "8d9333c6-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:A10",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "A10"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2764/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2764/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2765",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2765"},
                "attributes": {
                    "uuid": "8d9501b0-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:B10",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "B10"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2765/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2765/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2766",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2766"},
                "attributes": {
                    "uuid": "8d96d1e8-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:C10",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "C10"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2766/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2766/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2767",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2767"},
                "attributes": {
                    "uuid": "8d99d00a-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:D10",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "D10"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2767/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2767/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2768",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2768"},
                "attributes": {
                    "uuid": "8d9c198c-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:E10",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "E10"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2768/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2768/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2769",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2769"},
                "attributes": {
                    "uuid": "8d9e41c6-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:F10",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "F10"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2769/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2769/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2770",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2770"},
                "attributes": {
                    "uuid": "8da02bee-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:G10",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "G10"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2770/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2770/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2771",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2771"},
                "attributes": {
                    "uuid": "8da1f960-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:H10",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "H10"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2771/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2771/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2772",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2772"},
                "attributes": {
                    "uuid": "8da42802-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:A11",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "A11"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2772/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2772/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2773",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2773"},
                "attributes": {
                    "uuid": "8da7ac70-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:B11",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "B11"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2773/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2773/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2774",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2774"},
                "attributes": {
                    "uuid": "8daa5830-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:C11",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "C11"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2774/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2774/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2775",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2775"},
                "attributes": {
                    "uuid": "8dada350-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:D11",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "D11"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2775/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2775/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2776",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2776"},
                "attributes": {
                    "uuid": "8dafa268-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:E11",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "E11"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2776/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2776/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2777",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2777"},
                "attributes": {
                    "uuid": "8db1c7dc-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:F11",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "F11"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2777/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2777/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2778",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2778"},
                "attributes": {
                    "uuid": "8db3ce74-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:G11",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "G11"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2778/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2778/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2779",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2779"},
                "attributes": {
                    "uuid": "8db7ddb6-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:H11",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "H11"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2779/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2779/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2780",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2780"},
                "attributes": {
                    "uuid": "8db9fcd6-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:A12",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "A12"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2780/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2780/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2781",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2781"},
                "attributes": {
                    "uuid": "8dbc3014-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:B12",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "B12"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2781/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2781/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2782",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2782"},
                "attributes": {
                    "uuid": "8dbe94f8-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:C12",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "C12"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2782/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2782/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2783",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2783"},
                "attributes": {
                    "uuid": "8dc06e5e-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:D12",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "D12"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2783/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2783/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2784",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2784"},
                "attributes": {
                    "uuid": "8dc23824-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:E12",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "E12"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2784/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2784/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2785",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2785"},
                "attributes": {
                    "uuid": "8dc49d3a-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:F12",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "F12"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2785/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2785/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2786",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2786"},
                "attributes": {
                    "uuid": "8dc6630e-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:G12",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "G12"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2786/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2786/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "2787",
                "type": "wells",
                "links": {"self": "http://127.0.0.1:3000/api/v2/wells/2787"},
                "attributes": {
                    "uuid": "8dc84868-d9fd-11ed-9bf8-acde48001122",
                    "name": "SQPD-9014:H12",
                    "pcr_cycles": null,
                    "submit_for_sequencing": null,
                    "sub_pool": null,
                    "coverage": null,
                    "diluent_volume": null,
                    "state": "unknown",
                    "position": {"name": "H12"},
                },
                "relationships": {
                    "samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/samples",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/samples",
                        }
                    },
                    "studies": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/studies",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/studies",
                        }
                    },
                    "projects": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/projects",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/projects",
                        }
                    },
                    "requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/requests_as_source",
                        }
                    },
                    "requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/requests_as_target",
                        }
                    },
                    "qc_results": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/qc_results",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/qc_results",
                        }
                    },
                    "aliquots": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/aliquots",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/aliquots",
                        },
                        "data": [],
                    },
                    "downstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/downstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/downstream_assets",
                        }
                    },
                    "downstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/downstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/downstream_wells",
                        }
                    },
                    "downstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/downstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/downstream_plates",
                        }
                    },
                    "downstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/downstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/downstream_tubes",
                        }
                    },
                    "upstream_assets": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/upstream_assets",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/upstream_assets",
                        }
                    },
                    "upstream_wells": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/upstream_wells",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/upstream_wells",
                        }
                    },
                    "upstream_plates": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/upstream_plates",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/upstream_plates",
                        }
                    },
                    "upstream_tubes": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/upstream_tubes",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/upstream_tubes",
                        }
                    },
                    "transfer_requests_as_source": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/transfer_requests_as_source",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/transfer_requests_as_source",
                        }
                    },
                    "transfer_requests_as_target": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/wells/2787/relationships/transfer_requests_as_target",
                            "related": "http://127.0.0.1:3000/api/v2/wells/2787/transfer_requests_as_target",
                        }
                    },
                },
            },
            {
                "id": "123",
                "type": "aliquots",
                "links": {"self": "http://127.0.0.1:3000/api/v2/aliquots/123"},
                "attributes": {
                    "tag_oligo": null,
                    "tag_index": null,
                    "tag2_oligo": null,
                    "tag2_index": null,
                    "suboptimal": false,
                    "library_type": null,
                },
                "relationships": {
                    "study": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/123/relationships/study",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/123/study",
                        }
                    },
                    "project": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/123/relationships/project",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/123/project",
                        }
                    },
                    "sample": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/123/relationships/sample",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/123/sample",
                        },
                        "data": {"type": "samples", "id": "109"},
                    },
                    "request": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/123/relationships/request",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/123/request",
                        }
                    },
                },
            },
            {
                "id": "124",
                "type": "aliquots",
                "links": {"self": "http://127.0.0.1:3000/api/v2/aliquots/124"},
                "attributes": {
                    "tag_oligo": null,
                    "tag_index": null,
                    "tag2_oligo": null,
                    "tag2_index": null,
                    "suboptimal": false,
                    "library_type": null,
                },
                "relationships": {
                    "study": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/124/relationships/study",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/124/study",
                        }
                    },
                    "project": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/124/relationships/project",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/124/project",
                        }
                    },
                    "sample": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/124/relationships/sample",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/124/sample",
                        },
                        "data": {"type": "samples", "id": "110"},
                    },
                    "request": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/124/relationships/request",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/124/request",
                        }
                    },
                },
            },
            {
                "id": "125",
                "type": "aliquots",
                "links": {"self": "http://127.0.0.1:3000/api/v2/aliquots/125"},
                "attributes": {
                    "tag_oligo": null,
                    "tag_index": null,
                    "tag2_oligo": null,
                    "tag2_index": null,
                    "suboptimal": false,
                    "library_type": null,
                },
                "relationships": {
                    "study": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/125/relationships/study",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/125/study",
                        }
                    },
                    "project": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/125/relationships/project",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/125/project",
                        }
                    },
                    "sample": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/125/relationships/sample",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/125/sample",
                        },
                        "data": {"type": "samples", "id": "111"},
                    },
                    "request": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/125/relationships/request",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/125/request",
                        }
                    },
                },
            },
            {
                "id": "126",
                "type": "aliquots",
                "links": {"self": "http://127.0.0.1:3000/api/v2/aliquots/126"},
                "attributes": {
                    "tag_oligo": null,
                    "tag_index": null,
                    "tag2_oligo": null,
                    "tag2_index": null,
                    "suboptimal": false,
                    "library_type": null,
                },
                "relationships": {
                    "study": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/126/relationships/study",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/126/study",
                        }
                    },
                    "project": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/126/relationships/project",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/126/project",
                        }
                    },
                    "sample": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/126/relationships/sample",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/126/sample",
                        },
                        "data": {"type": "samples", "id": "112"},
                    },
                    "request": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/aliquots/126/relationships/request",
                            "related": "http://127.0.0.1:3000/api/v2/aliquots/126/request",
                        }
                    },
                },
            },
            {
                "id": "109",
                "type": "samples",
                "links": {"self": "http://127.0.0.1:3000/api/v2/samples/109"},
                "attributes": {
                    "name": "2STDY193",
                    "sanger_sample_id": "2STDY193",
                    "uuid": "f0eb25fa-d9fd-11ed-9d29-acde48001122",
                    "control": true,
                    "control_type": "pcr positive",
                },
                "relationships": {
                    "sample_metadata": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/samples/109/relationships/sample_metadata",
                            "related": "http://127.0.0.1:3000/api/v2/samples/109/sample_metadata",
                        }
                    },
                    "sample_manifest": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/samples/109/relationships/sample_manifest",
                            "related": "http://127.0.0.1:3000/api/v2/samples/109/sample_manifest",
                        }
                    },
                    "component_samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/samples/109/relationships/component_samples",
                            "related": "http://127.0.0.1:3000/api/v2/samples/109/component_samples",
                        }
                    },
                },
            },
            {
                "id": "110",
                "type": "samples",
                "links": {"self": "http://127.0.0.1:3000/api/v2/samples/110"},
                "attributes": {
                    "name": "2STDY194",
                    "sanger_sample_id": "2STDY194",
                    "uuid": "f0ef2b32-d9fd-11ed-9d29-acde48001122",
                    "control": true,
                    "control_type": "pcr negative",
                },
                "relationships": {
                    "sample_metadata": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/samples/110/relationships/sample_metadata",
                            "related": "http://127.0.0.1:3000/api/v2/samples/110/sample_metadata",
                        }
                    },
                    "sample_manifest": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/samples/110/relationships/sample_manifest",
                            "related": "http://127.0.0.1:3000/api/v2/samples/110/sample_manifest",
                        }
                    },
                    "component_samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/samples/110/relationships/component_samples",
                            "related": "http://127.0.0.1:3000/api/v2/samples/110/component_samples",
                        }
                    },
                },
            },
            {
                "id": "111",
                "type": "samples",
                "links": {"self": "http://127.0.0.1:3000/api/v2/samples/111"},
                "attributes": {
                    "name": "2STDY195",
                    "sanger_sample_id": "2STDY195",
                    "uuid": "f0f2dfd4-d9fd-11ed-9d29-acde48001122",
                    "control": false,
                    "control_type": null,
                },
                "relationships": {
                    "sample_metadata": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/samples/111/relationships/sample_metadata",
                            "related": "http://127.0.0.1:3000/api/v2/samples/111/sample_metadata",
                        }
                    },
                    "sample_manifest": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/samples/111/relationships/sample_manifest",
                            "related": "http://127.0.0.1:3000/api/v2/samples/111/sample_manifest",
                        }
                    },
                    "component_samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/samples/111/relationships/component_samples",
                            "related": "http://127.0.0.1:3000/api/v2/samples/111/component_samples",
                        }
                    },
                },
            },
            {
                "id": "112",
                "type": "samples",
                "links": {"self": "http://127.0.0.1:3000/api/v2/samples/112"},
                "attributes": {
                    "name": "2STDY196",
                    "sanger_sample_id": "2STDY196",
                    "uuid": "f0f61f32-d9fd-11ed-9d29-acde48001122",
                    "control": false,
                    "control_type": null,
                },
                "relationships": {
                    "sample_metadata": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/samples/112/relationships/sample_metadata",
                            "related": "http://127.0.0.1:3000/api/v2/samples/112/sample_metadata",
                        }
                    },
                    "sample_manifest": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/samples/112/relationships/sample_manifest",
                            "related": "http://127.0.0.1:3000/api/v2/samples/112/sample_manifest",
                        }
                    },
                    "component_samples": {
                        "links": {
                            "self": "http://127.0.0.1:3000/api/v2/samples/112/relationships/component_samples",
                            "related": "http://127.0.0.1:3000/api/v2/samples/112/component_samples",
                        }
                    },
                },
            },
        ],
    }

    mocked_responses.add(responses.GET, ss_url, json=body, status=HTTPStatus.OK)

    response = client.post(endpoint, json={"user": "user1", "robot": "robot1", "barcode": barcode})

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"barcode": "SQPD-9014", "positive_control": "A1", "negative_control": "B1"}