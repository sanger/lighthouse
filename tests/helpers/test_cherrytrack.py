from http import HTTPStatus

import responses

from lighthouse.helpers.cherrytrack import (
    get_automation_system_run_info_from_cherrytrack,
    get_samples_from_source_plate_barcode_from_cherrytrack,
    get_wells_from_destination_barcode_from_cherrytrack,
)


def test_get_automation_system_run_info_from_cherrytrack(app):
    with app.app_context():
        run_id = 1
        response = get_automation_system_run_info_from_cherrytrack(run_id)

        assert response.json() == {
            "data": {
                "automation_system_manufacturer": "biosero",
                "automation_system_name": "CPA",
                "id": 1,
                "liquid_handler_serial_number": "LHS000001",
                "user_id": "ab12",
            }
        }


def test_get_samples_from_source_plate_barcode_from_cherrytrack(app):
    with app.app_context():
        source_plate_barcode = "DS000010003"
        response = get_samples_from_source_plate_barcode_from_cherrytrack(source_plate_barcode)

        assert response.json() == {
            "data": {
                "barcode": "DS000010003",
                "samples": [
                    {
                        "automation_system_run_id": 1,
                        "destination_barcode": "DN00000001",
                        "destination_coordinate": "H6",
                        "lab_id": "MK",
                        "picked": True,
                        "rna_id": "RNA-S-00001-00000004",
                        "sample_id": "c15a694f-a4db-44f4-9a98-6c1804197f01",
                        "source_barcode": "DS000010003",
                        "source_coordinate": "A4",
                        "type": "sample",
                    },
                    {
                        "automation_system_run_id": 1,
                        "destination_barcode": "DN00000001",
                        "destination_coordinate": "H3",
                        "lab_id": "MK",
                        "picked": True,
                        "rna_id": "RNA-S-00001-00000001",
                        "sample_id": "c4cc673e-3da0-47da-b754-ae01b7c6095e",
                        "source_barcode": "DS000010003",
                        "source_coordinate": "A6",
                        "type": "sample",
                    },
                    {
                        "automation_system_run_id": 1,
                        "destination_barcode": "DN00000001",
                        "destination_coordinate": "H12",
                        "lab_id": "MK",
                        "picked": True,
                        "rna_id": "RNA-S-00001-00000009",
                        "sample_id": "da95a299-1ad4-4620-aaf1-4ba7ab21522f",
                        "source_barcode": "DS000010003",
                        "source_coordinate": "B4",
                        "type": "sample",
                    },
                    {
                        "automation_system_run_id": 1,
                        "destination_barcode": "DN00000001",
                        "destination_coordinate": "H8",
                        "lab_id": "MK",
                        "picked": True,
                        "rna_id": "RNA-S-00001-00000006",
                        "sample_id": "5e9d1b1a-2c32-4921-87f5-770032bec951",
                        "source_barcode": "DS000010003",
                        "source_coordinate": "C7",
                        "type": "sample",
                    },
                    {
                        "automation_system_run_id": 1,
                        "destination_barcode": "DN00000001",
                        "destination_coordinate": "H10",
                        "lab_id": "MK",
                        "picked": True,
                        "rna_id": "RNA-S-00001-00000008",
                        "sample_id": "9f1ed0d9-40f2-4019-a1dc-2b2288a76d59",
                        "source_barcode": "DS000010003",
                        "source_coordinate": "D3",
                        "type": "sample",
                    },
                    {
                        "automation_system_run_id": "",
                        "destination_barcode": "",
                        "destination_coordinate": "",
                        "lab_id": "MK",
                        "picked": False,
                        "rna_id": "RNA-S-00001-00000010",
                        "sample_id": "8d077231-9202-4115-9848-8095153693cb",
                        "source_barcode": "DS000010003",
                        "source_coordinate": "D7",
                        "type": "sample",
                    },
                    {
                        "automation_system_run_id": 1,
                        "destination_barcode": "DN00000001",
                        "destination_coordinate": "H7",
                        "lab_id": "MK",
                        "picked": True,
                        "rna_id": "RNA-S-00001-00000005",
                        "sample_id": "33f2c6e2-5391-4a80-bc55-d60025f6b790",
                        "source_barcode": "DS000010003",
                        "source_coordinate": "D11",
                        "type": "sample",
                    },
                    {
                        "automation_system_run_id": 1,
                        "destination_barcode": "DN00000001",
                        "destination_coordinate": "H5",
                        "lab_id": "MK",
                        "picked": True,
                        "rna_id": "RNA-S-00001-00000003",
                        "sample_id": "3eef31b7-1426-4579-b9a9-4fb895bdde21",
                        "source_barcode": "DS000010003",
                        "source_coordinate": "E9",
                        "type": "sample",
                    },
                    {
                        "automation_system_run_id": 1,
                        "destination_barcode": "DN00000001",
                        "destination_coordinate": "H9",
                        "lab_id": "MK",
                        "picked": True,
                        "rna_id": "RNA-S-00001-00000007",
                        "sample_id": "7057d944-e912-4bf8-9eea-466b701b57f3",
                        "source_barcode": "DS000010003",
                        "source_coordinate": "F12",
                        "type": "sample",
                    },
                    {
                        "automation_system_run_id": 1,
                        "destination_barcode": "DN00000001",
                        "destination_coordinate": "H4",
                        "lab_id": "MK",
                        "picked": True,
                        "rna_id": "RNA-S-00001-00000002",
                        "sample_id": "1fc8e19d-a21e-4a71-9d7d-e19965805ea9",
                        "source_barcode": "DS000010003",
                        "source_coordinate": "G1",
                        "type": "sample",
                    },
                    {
                        "automation_system_run_id": "",
                        "destination_barcode": "",
                        "destination_coordinate": "",
                        "lab_id": "MK",
                        "picked": False,
                        "rna_id": "RNA-S-00001-00000011",
                        "sample_id": "ef6e8c63-6d15-49ab-b5a1-599a1625af33",
                        "source_barcode": "DS000010003",
                        "source_coordinate": "G9",
                        "type": "sample",
                    },
                ],
            }
        }


def test_get_wells_from_destination_barcode_from_cherrytrack(app):
    with app.app_context():
        destination_plate_barcode = "DN00000001"
        response = get_wells_from_destination_barcode_from_cherrytrack(destination_plate_barcode)

        assert response.json() == {
            "data": {

								"barcode": "DN00000001",
                "wells": [
                    {
              "automation_system_run_id": 1,
              "destination_coordinate": "A1",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000001",
              "sample_id": "42a42168-3b75-4425-960b-b2be94249309",
              "source_barcode": "DS000010001",
              "source_coordinate": "H2",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "A2",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000002",
              "sample_id": "a93ba9f9-757e-4eb6-9d40-489110758502",
              "source_barcode": "DS000010001",
              "source_coordinate": "D12",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "A3",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000003",
              "sample_id": "07624bfa-e0d6-48cc-b612-38ce25c8274a",
              "source_barcode": "DS000010001",
              "source_coordinate": "G6",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "A4",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000004",
              "sample_id": "5d8541de-3a8f-4536-80d3-e451cec2d0c0",
              "source_barcode": "DS000010001",
              "source_coordinate": "E6",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "A5",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000005",
              "sample_id": "1b7f5f63-e44b-4ae8-8f98-337ac1c55594",
              "source_barcode": "DS000010001",
              "source_coordinate": "G10",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "A6",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000006",
              "sample_id": "bdc88f7c-eebc-428f-a965-809931812c5d",
              "source_barcode": "DS000010001",
              "source_coordinate": "F12",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "A7",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000007",
              "sample_id": "7422de3b-d58f-42c3-b232-b5d53a25027a",
              "source_barcode": "DS000010001",
              "source_coordinate": "H1",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "A8",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000008",
              "sample_id": "d6f461b9-576f-499f-b75e-88c7972a07f5",
              "source_barcode": "DS000010001",
              "source_coordinate": "E3",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "A9",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000009",
              "sample_id": "c590d5d0-b699-4371-b904-817015994395",
              "source_barcode": "DS000010001",
              "source_coordinate": "A7",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "A10",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000010",
              "sample_id": "0a192a62-df6c-4d9b-b4b8-f2ae2d03a69d",
              "source_barcode": "DS000010001",
              "source_coordinate": "F11",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "A11",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000011",
              "sample_id": "0b5dfbac-19ed-4deb-a220-5aaab4dce38a",
              "source_barcode": "DS000010001",
              "source_coordinate": "A2",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "A12",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000012",
              "sample_id": "f1e31b5a-ff2e-4de9-b962-3f8d84335fb6",
              "source_barcode": "DS000010001",
              "source_coordinate": "D11",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "B1",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000013",
              "sample_id": "44aae446-658f-460d-bc15-de8b923bb496",
              "source_barcode": "DS000010001",
              "source_coordinate": "F6",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "B2",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000014",
              "sample_id": "36234f97-6311-4997-870d-bf8045fb9e53",
              "source_barcode": "DS000010001",
              "source_coordinate": "F9",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "B3",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000015",
              "sample_id": "8707d866-27a8-4cc0-9709-c28a486a1396",
              "source_barcode": "DS000010001",
              "source_coordinate": "E4",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "B4",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000016",
              "sample_id": "1cdd1a8b-8e7a-4091-b062-2d1d31cab4b6",
              "source_barcode": "DS000010001",
              "source_coordinate": "B8",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "control": "negative",
              "control_barcode": "DN999999999",
              "control_coordinate": "H12",
              "destination_coordinate": "B5",
              "type": "control"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "B6",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000017",
              "sample_id": "608b704b-cf0e-4d03-a00b-5a88e48e1079",
              "source_barcode": "DS000010001",
              "source_coordinate": "E2",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "B7",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000018",
              "sample_id": "20dd3cc2-0d06-41b1-b925-cc05475b3bb9",
              "source_barcode": "DS000010001",
              "source_coordinate": "H5",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "B8",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000019",
              "sample_id": "a6bd06e2-d818-4c50-b16a-a3ab550f7f8b",
              "source_barcode": "DS000010001",
              "source_coordinate": "D7",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "B9",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000020",
              "sample_id": "18c447e2-ac0b-4293-9c00-03de672a570c",
              "source_barcode": "DS000010001",
              "source_coordinate": "D5",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "B10",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000021",
              "sample_id": "98145b14-1803-473b-a8de-6fefe5de824b",
              "source_barcode": "DS000010001",
              "source_coordinate": "E12",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "B11",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000022",
              "sample_id": "737e34e2-d52f-40c0-8de0-cf2d43d4afd8",
              "source_barcode": "DS000010001",
              "source_coordinate": "B2",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "B12",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000023",
              "sample_id": "19a5c91d-40ab-4954-9cee-880f93526b57",
              "source_barcode": "DS000010001",
              "source_coordinate": "F3",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "C1",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000024",
              "sample_id": "71a53bf7-463a-4e86-8a58-1dd56716f846",
              "source_barcode": "DS000010001",
              "source_coordinate": "E5",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "C2",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000025",
              "sample_id": "82e201c0-623f-4a0a-930f-620122bc5c92",
              "source_barcode": "DS000010001",
              "source_coordinate": "F2",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "C3",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000026",
              "sample_id": "b502a247-a1fc-4168-933d-af2c46061f3a",
              "source_barcode": "DS000010001",
              "source_coordinate": "D2",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "C4",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000027",
              "sample_id": "400efa77-9e2b-48ca-8087-39c9e775c0fc",
              "source_barcode": "DS000010001",
              "source_coordinate": "H11",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "C5",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000028",
              "sample_id": "996c210c-42b1-4a29-bf61-35777f3c8834",
              "source_barcode": "DS000010001",
              "source_coordinate": "B3",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "C6",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000029",
              "sample_id": "a3afd596-1ce0-495a-bfcc-4c7bf1c160f5",
              "source_barcode": "DS000010001",
              "source_coordinate": "G5",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "C7",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000030",
              "sample_id": "79ce6fe0-c8da-4a84-9fdf-b6b50f4fb687",
              "source_barcode": "DS000010001",
              "source_coordinate": "A8",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "C8",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000031",
              "sample_id": "52958db6-b0fc-42e6-aff5-3c5b433ffa48",
              "source_barcode": "DS000010001",
              "source_coordinate": "B10",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "C9",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000032",
              "sample_id": "eec4bd76-2089-4b70-afe1-26f80b7d6ae3",
              "source_barcode": "DS000010001",
              "source_coordinate": "B1",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "C10",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000033",
              "sample_id": "53e53b0d-002d-4043-952d-bff4d51ab979",
              "source_barcode": "DS000010001",
              "source_coordinate": "C11",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "C11",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000034",
              "sample_id": "d04cc6d8-d2ec-4559-a15c-0ffa03d00b42",
              "source_barcode": "DS000010001",
              "source_coordinate": "H6",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "C12",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000035",
              "sample_id": "8f76037d-2cd5-405f-885c-507ffe53e883",
              "source_barcode": "DS000010001",
              "source_coordinate": "C3",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "D1",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000036",
              "sample_id": "9c23a5a5-2e69-4283-b899-01a42472f074",
              "source_barcode": "DS000010001",
              "source_coordinate": "G4",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "D2",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000037",
              "sample_id": "3c573228-7cc0-4c09-9e14-da5b7f4c3da8",
              "source_barcode": "DS000010001",
              "source_coordinate": "E7",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "D3",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000038",
              "sample_id": "642ef251-45eb-49e2-bd2e-d1079ba1aeda",
              "source_barcode": "DS000010001",
              "source_coordinate": "H3",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "D4",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000039",
              "sample_id": "c20152eb-e2d6-4fe9-a34d-c0ab00acfe0b",
              "source_barcode": "DS000010001",
              "source_coordinate": "F7",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "D5",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000040",
              "sample_id": "f3013c12-f7df-4022-914e-8b924718b045",
              "source_barcode": "DS000010001",
              "source_coordinate": "C6",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "D6",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000041",
              "sample_id": "9a179390-1070-4013-aff5-b0929705657d",
              "source_barcode": "DS000010001",
              "source_coordinate": "C5",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "D7",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000042",
              "sample_id": "a5f4ee74-2475-422a-9b25-eadf359a314f",
              "source_barcode": "DS000010001",
              "source_coordinate": "G12",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "D8",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000043",
              "sample_id": "e944dbf7-9cc9-49d4-8cd4-923b0eb90d8d",
              "source_barcode": "DS000010001",
              "source_coordinate": "G2",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "D9",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000044",
              "sample_id": "cdfcc77a-a5ad-4026-a20d-3bbf0ca20908",
              "source_barcode": "DS000010001",
              "source_coordinate": "E10",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "D10",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000045",
              "sample_id": "5e32de0d-14b5-4996-89ca-9f5fe9ce1065",
              "source_barcode": "DS000010001",
              "source_coordinate": "G1",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "D11",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000046",
              "sample_id": "01b4f9f8-6f2f-439c-9dfa-4b08ea93ea19",
              "source_barcode": "DS000010001",
              "source_coordinate": "C9",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "D12",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000047",
              "sample_id": "5986a19a-8866-45fc-a4cc-57d562374958",
              "source_barcode": "DS000010001",
              "source_coordinate": "B9",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "E1",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000048",
              "sample_id": "8c7aa57c-00ee-4879-a895-c8b332a7a699",
              "source_barcode": "DS000010001",
              "source_coordinate": "A6",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "E2",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000049",
              "sample_id": "8c5db67f-90f6-4528-b221-645169867dad",
              "source_barcode": "DS000010001",
              "source_coordinate": "E1",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "E3",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000050",
              "sample_id": "2794b94b-47e0-4ed4-b479-605d77cb9ff7",
              "source_barcode": "DS000010001",
              "source_coordinate": "H4",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "E4",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000051",
              "sample_id": "99ae8f8b-7f78-4d9a-a42a-9fefcb05859d",
              "source_barcode": "DS000010001",
              "source_coordinate": "A1",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "E5",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000052",
              "sample_id": "b2af9ffe-b2e0-49ba-b4bd-6cb85e22d413",
              "source_barcode": "DS000010001",
              "source_coordinate": "F4",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "E6",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000053",
              "sample_id": "60657a92-1d53-49b7-b772-3b0883fa1d37",
              "source_barcode": "DS000010001",
              "source_coordinate": "D1",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "E7",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000054",
              "sample_id": "de96f1a4-9a84-4ac1-929b-cce2c98b0ab6",
              "source_barcode": "DS000010001",
              "source_coordinate": "D4",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "E8",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000055",
              "sample_id": "b6257e09-9b13-4aed-96a6-6dbedfaa3038",
              "source_barcode": "DS000010001",
              "source_coordinate": "E9",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "E9",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000056",
              "sample_id": "09e3a751-dacb-4714-b9b3-d5e2f28a91dd",
              "source_barcode": "DS000010001",
              "source_coordinate": "F1",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "E10",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000057",
              "sample_id": "286cb73a-9b3c-407d-b01e-6d99e126dd75",
              "source_barcode": "DS000010001",
              "source_coordinate": "A9",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "E11",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000058",
              "sample_id": "9211292f-597f-4166-9c45-43e1d683cafd",
              "source_barcode": "DS000010001",
              "source_coordinate": "C4",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "E12",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000059",
              "sample_id": "f5bc3a32-9dcd-4e06-9f1c-3b4fbabaf242",
              "source_barcode": "DS000010001",
              "source_coordinate": "C8",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "F1",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000060",
              "sample_id": "449509b3-ac00-40e9-a168-31f01c0aa3bb",
              "source_barcode": "DS000010001",
              "source_coordinate": "A3",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "F2",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000061",
              "sample_id": "65d042c7-87f1-425d-b24a-c482b50a60cd",
              "source_barcode": "DS000010001",
              "source_coordinate": "A5",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "F3",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000062",
              "sample_id": "4c3d1b10-1493-4855-9ce1-a3194db69791",
              "source_barcode": "DS000010001",
              "source_coordinate": "F10",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "F4",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000063",
              "sample_id": "8a6fd4c6-f997-488d-877f-605cc359bf2f",
              "source_barcode": "DS000010001",
              "source_coordinate": "E8",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "F5",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000064",
              "sample_id": "aede1431-23c9-4419-82e1-16391b85a2cb",
              "source_barcode": "DS000010001",
              "source_coordinate": "B6",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "F6",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000065",
              "sample_id": "8acc6e89-dfd0-46f1-8505-f1e65ee8b69b",
              "source_barcode": "DS000010001",
              "source_coordinate": "H8",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "F7",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000001",
              "sample_id": "18efa4bf-9dd7-43cf-b5bd-6a2a37406a3c",
              "source_barcode": "DS000010002",
              "source_coordinate": "E8",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "F8",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000002",
              "sample_id": "9673317f-d273-48a9-9d6e-d2013ec38a54",
              "source_barcode": "DS000010002",
              "source_coordinate": "B4",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "F9",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000003",
              "sample_id": "dbb989fc-54bd-4f5f-b4f9-8b13acacf24c",
              "source_barcode": "DS000010002",
              "source_coordinate": "B12",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "F10",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000004",
              "sample_id": "2272dbbc-5347-4920-a443-b6aac9de1236",
              "source_barcode": "DS000010002",
              "source_coordinate": "D10",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "F11",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000005",
              "sample_id": "4529c430-0421-4991-b838-ff080bfb4d33",
              "source_barcode": "DS000010002",
              "source_coordinate": "H9",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "F12",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000006",
              "sample_id": "87f49f0d-a525-4247-aca3-8055f74c1ee4",
              "source_barcode": "DS000010002",
              "source_coordinate": "G9",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "G1",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000007",
              "sample_id": "e3adca9e-4d71-4fdd-847c-76fbeaf990f3",
              "source_barcode": "DS000010002",
              "source_coordinate": "D2",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "G2",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000008",
              "sample_id": "634f44e8-5820-40b8-a545-8d313ace7d86",
              "source_barcode": "DS000010002",
              "source_coordinate": "B2",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "G3",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000009",
              "sample_id": "dc60d6c2-42f5-4e7c-a166-28296dc34ab1",
              "source_barcode": "DS000010002",
              "source_coordinate": "F3",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "G4",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000010",
              "sample_id": "c4836a7a-1fed-470e-965d-a9769933d47b",
              "source_barcode": "DS000010002",
              "source_coordinate": "F4",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "G5",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000011",
              "sample_id": "92ae272a-0591-46d8-ac6d-a254e5a4f0ea",
              "source_barcode": "DS000010002",
              "source_coordinate": "G4",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "G6",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000012",
              "sample_id": "efd71bc7-5393-40d9-b1c0-695b5b565181",
              "source_barcode": "DS000010002",
              "source_coordinate": "A12",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "G7",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000013",
              "sample_id": "bdfdf1e3-07c9-4508-b781-e3f0676225ac",
              "source_barcode": "DS000010002",
              "source_coordinate": "A4",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "G8",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000014",
              "sample_id": "0d5bbe32-5376-49ee-9636-5c0a0bacf22e",
              "source_barcode": "DS000010002",
              "source_coordinate": "A3",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "G9",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000015",
              "sample_id": "a1f801b2-5cbb-4b6a-b302-30aacb59cb3a",
              "source_barcode": "DS000010002",
              "source_coordinate": "E10",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "G10",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000016",
              "sample_id": "cf0bd84a-e567-4801-887c-38d999dbc5db",
              "source_barcode": "DS000010002",
              "source_coordinate": "F5",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "G11",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000017",
              "sample_id": "eab923d7-c197-4bdd-b281-28e568c777ce",
              "source_barcode": "DS000010002",
              "source_coordinate": "H7",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "G12",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000018",
              "sample_id": "b1750fbf-7dd2-4721-8d55-a9e9acf240e8",
              "source_barcode": "DS000010002",
              "source_coordinate": "D5",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "H1",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000019",
              "sample_id": "701d9706-0708-412a-918b-1afce4163fb8",
              "source_barcode": "DS000010002",
              "source_coordinate": "C11",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "H2",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000020",
              "sample_id": "8fd4c6cf-d01d-4fd2-9eca-8c84ce91545e",
              "source_barcode": "DS000010002",
              "source_coordinate": "B3",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "H3",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000001",
              "sample_id": "c4cc673e-3da0-47da-b754-ae01b7c6095e",
              "source_barcode": "DS000010003",
              "source_coordinate": "A6",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "H4",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000002",
              "sample_id": "1fc8e19d-a21e-4a71-9d7d-e19965805ea9",
              "source_barcode": "DS000010003",
              "source_coordinate": "G1",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "H5",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000003",
              "sample_id": "3eef31b7-1426-4579-b9a9-4fb895bdde21",
              "source_barcode": "DS000010003",
              "source_coordinate": "E9",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "H6",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000004",
              "sample_id": "c15a694f-a4db-44f4-9a98-6c1804197f01",
              "source_barcode": "DS000010003",
              "source_coordinate": "A4",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "H7",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000005",
              "sample_id": "33f2c6e2-5391-4a80-bc55-d60025f6b790",
              "source_barcode": "DS000010003",
              "source_coordinate": "D11",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "H8",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000006",
              "sample_id": "5e9d1b1a-2c32-4921-87f5-770032bec951",
              "source_barcode": "DS000010003",
              "source_coordinate": "C7",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "H9",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000007",
              "sample_id": "7057d944-e912-4bf8-9eea-466b701b57f3",
              "source_barcode": "DS000010003",
              "source_coordinate": "F12",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "H10",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000008",
              "sample_id": "9f1ed0d9-40f2-4019-a1dc-2b2288a76d59",
              "source_barcode": "DS000010003",
              "source_coordinate": "D3",
              "type": "sample"
            },
            {
              "automation_system_run_id": 1,
              "control": "positive",
              "control_barcode": "DN999999999",
              "control_coordinate": "A1",
              "destination_coordinate": "H11",
              "type": "control"
            },
            {
              "automation_system_run_id": 1,
              "destination_coordinate": "H12",
              "lab_id": "MK",
              "rna_id": "RNA-S-00001-00000009",
              "sample_id": "da95a299-1ad4-4620-aaf1-4ba7ab21522f",
              "source_barcode": "DS000010003",
              "source_coordinate": "B4",
              "type": "sample"
            }
          ]
        }
}



