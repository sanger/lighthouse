if not exists (SELECT Name
from sys.tables
where Name='CherrypickingInfo') CREATE TABLE CherrypickingInfo
(
  destination_barcode NVARCHAR(50),
  destination_coordinate NVARCHAR(50),
  source_barcode NVARCHAR(50),
  source_coordinate NVARCHAR(50),
  control NVARCHAR(50),
  root_sample_id NVARCHAR(50),
  rna_id NVARCHAR(50),
  lab_id NVARCHAR(50),
);

