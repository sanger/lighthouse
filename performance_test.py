import json


def test_create_testing_files():
    i = 0
    lots_declarations = []
    samples_declarations = []
    while i < 100000:
        lots_declarations.append(
            {
                "root_sample_id": f"MCM00{i}",
                "value_in_sequencing": "Yes",
                "declared_at": "2013-04-04T10:29:13",
            }
        )
        samples_declarations.append(
            {
                "coordinate": "A01",
                "source": "test1",
                "Result": "Positive",
                "plate_barcode": "123",
                "barcode": "abc",
                "Root Sample ID": f"MCM00{i}",
            }
        )
        i = i + 1

    with open("declarations.txt", "w") as outfile:
        json.dump(lots_declarations, outfile)

    with open("samples.txt", "w") as outfile:
        json.dump(samples_declarations, outfile)


test_create_testing_files()
