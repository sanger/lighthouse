# Data Fix Scripts
## **Intro**
The Python scripts in this folder provide the basis for correcting data in the MLWH and MongoDB databases. They aren't fit for the purpose of deleting data, simply for updating fields where there is malformed data.

The general workflow that these scripts support is
1. **get the data, fix it and save it to a local CSV**
2. **update the database using the local CSV**

There are also scripts which are useful for populating and testing local databases with dummy data, so the user can ensure that the fixes will work, and that bugs are fixed, before deploying to UAT/Prod environments.

This guide assumes that you have set up the Lighthouse repository as per [the main README file](../../../README.md)

## **Usage**
### Setup

Before getting started:

- To be able to connect to the databases and access the relevant local files, the scripts need environment variables saved in a local file called _constants.py_, saved in the top level of the `data-fixes` folder. Since this git repository is public, this file is ignored by git - otherwise DB connection details would be made public. You can create your own file using the _constants_template.py_ file in this `user-guide` directory.

- Ensure connection details are correct in _constants.py_. The environment variables stored under the "## Exported / Used ---" comment are actually used in the scripts. The variables above this comment are used to save the user time when it comes to finding credentials/URLs etc. The templates file shows an example of setting the exported credentials to that of the local databases.

### Fixing and Saving Data
1. Run `python ./data-fixes/save_data_locally.py --input_filename="..." --output_filename="..."`. The `output_filename` argument is the file that the data will be written to, and should be CSV (note if it already exists it will be overwritten). The `input_filename` argument is optional - it should be used if the data you are trying to fix is already saved locally (i.e. you have already run a SQL call and downloaded the results locally). If you do not enter an `input_filename` argument, the script will call the database itself using the `get_data()` function, which uses the `SQL_MLWH_GET_MALFORMED_DATA` environment variable from _constants.py_.

2. This script will apply any fixes in the `save_data()` function, before saving it to `output_filename`. You can add lines of fixes to this method, or change which methods are applied. The functions used for this are kept in _data_helpers.py_.


### Updating Database
1. There needs to be data in CSV format in a `data-fixes/data/` directory. The location of file should be listed under `fixed_data_file` in _constants.py_. At the very least this file should have two columns:
    - `root_sample_id`, `rna_id`, `lab_id` and `result` columns, which together define a unique row of data
    - a column with the corresponding fixed data. The names of this column should be listed in _constants.py_ under `FIXED_DATA_COL_NAME`.

    Meanwhile, the `MLWH_COLUMN_NAME` or `MONGO_COLUMN_NAME` variable in _constants.py_ should be set to the name of the field in the database of interest.

2. Run `python ./data-fixes/write_data_to_db.py --db='...'` where "..." is either "mysql" or "mongo".
