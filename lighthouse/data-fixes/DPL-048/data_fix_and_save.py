# get the root_sample_ids, fix them, write these to a CSV to be used with the 'write_data' script (which inserts the fixed IDs into the DBs)

from data_getters import get_data
from data_helpers import remove_everything_after_first_underscore

def save_data():
    data = get_data()
    print("Editing the root_sample_ids...")
    data = data.rename(columns={"root_sample_id": "original_root_sample_id"})
    data["root_sample_id"] = data["original_root_sample_id"].apply(remove_everything_after_first_underscore)
    print("Adding the root_sample_ids to a CSV file.")
    data.to_csv('data-fixes/test-data/root_sample_ids.csv', index=False)

if __name__ == "__main__":
    save_data()
