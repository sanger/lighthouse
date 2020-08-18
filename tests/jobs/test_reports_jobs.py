import pandas as pd
from lighthouse.jobs.reports import get_cherrypicked_samples
from unittest.mock import patch, Mock

def test_get_cherrypicked_samples(app, freezer):

  expected = pd.DataFrame(['MCM001', 'MCM003', 'MCM005'], columns=['description'], index=[0, 1, 2])
  samples = "MCM001,MCM002,MCM003,MCM004,MCM005"

  with app.app_context():
    with patch(
      "sqlalchemy.create_engine", return_value=Mock()
    ):
      with patch(
          "pandas.read_sql", return_value=expected,
        ):
        returned_samples = get_cherrypicked_samples(samples)
        assert returned_samples.at[0, 'description'] == "MCM001"
        assert returned_samples.at[1, 'description'] == "MCM003"
        assert returned_samples.at[2, 'description'] == "MCM005"
