# get the data, fix it, write these to a CSV to be used with the 'write_data' script (which inserts the fixed data into the DBs)
import pandas as pd
import argparse

from data_getters import get_data
from data_helpers import remove_everything_after_first_underscore

from constants import (
    COLUMN_NAME,
    ORIGINAL_COLUMN_NAME
)

def save_data(input_filename, output_filename):
    if input_filename:
        data = pd.read_csv(input_filename)
    else:
        data = get_data()

    print("Editing the data...")
    data = data.rename(columns={COLUMN_NAME: ORIGINAL_COLUMN_NAME})
    data[COLUMN_NAME] = data[ORIGINAL_COLUMN_NAME].apply(remove_everything_after_first_underscore)
    print("Adding the data to a CSV file.")
    data.to_csv(output_filename, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", required=False)
    parser.add_argument("--output_file", required=True)
    args = parser.parse_args()
    input_filename = vars(args)["input_file"]
    output_filename = vars(args)["output_file"]
    save_data(input_filename=input_filename, output_filename=output_filename)
