if not exists (SELECT Name
from sys.tables
where Name='CherrypickingInfo') CREATE TABLE CherrypickingInfo
(
  id INT,
  destination_barcode NVARCHAR(50),
  destination_coordinate NVARCHAR(50),
  source_barcode NVARCHAR(50),
  source_coordinate NVARCHAR(50),
  source_created_at NVARCHAR(50),
  source_evaluation_version NVARCHAR(50),
  cherrypicked_at NVARCHAR(50),
);

