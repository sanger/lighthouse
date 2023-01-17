PLATES_LOOKUP_WITHOUT_SAMPLES = {
    "plate_123": {
        "plate_barcode": "plate_123",
        "has_plate_map": True,
        "count_fit_to_pick_samples": 5,
        "count_filtered_positive": 3,
        "count_must_sequence": 2,
        "count_preferentially_sequence": 1,
    }
}

PLATES_LOOKUP_WITH_SAMPLES = {
    "plate_123": {
        "plate_barcode": "plate_123",
        "has_plate_map": True,
        "count_fit_to_pick_samples": 5,
        "count_filtered_positive": 3,
        "count_must_sequence": 2,
        "count_preferentially_sequence": 1,
        "pickable_samples": [
            {
                "lab_id": "lab_1",
                "rna_id": "rna_1",
                "sample_id": "0a53e7b6-7ce8-4ebc-95c3-02dd64942531",
                "source_coordinate_padded": "A01",
                "source_coordinate_unpadded": "A1",
            },
            {
                "lab_id": "lab_1",
                "rna_id": "rna_2",
                "sample_id": "1a53e7b6-7ce8-4ebc-95c3-02dd64942531",
                "source_coordinate_padded": "A02",
                "source_coordinate_unpadded": "A2",
            },
            {
                "lab_id": "lab_1",
                "rna_id": "rna_a",
                "sample_id": "8426ba76-e595-4475-92a6-8a60be0eee20",
                "source_coordinate_padded": "B01",
                "source_coordinate_unpadded": "B1",
            },
            {
                "lab_id": "lab_1",
                "rna_id": "rna_6",
                "sample_id": "2a53e7b6-7ce8-4ebc-95c3-02dd64942532",
                "source_coordinate_padded": "E01",
                "source_coordinate_unpadded": "E1",
            },
            {
                "lab_id": "lab_1",
                "rna_id": "rna_pl",
                "sample_id": "69855245-a66b-4172-ab46-a1d344b5ca8b",
                "source_coordinate_padded": "F01",
                "source_coordinate_unpadded": "F1",
            },
        ],
    }
}
