if not exists (SELECT Name
from sys.tables
where Name='CherrypickingInfo') CREATE TABLE CherrypickingInfo
(
  [Run-ID] int,
  [Labware BarCode] NVARCHAR(50),
  [Well Location] NVARCHAR(50),
  [Well Source Barcode] NVARCHAR(50),
  [Well Source Well] NVARCHAR(50),
  [Well control] NVARCHAR(50),
  [Well root_sample_id] NVARCHAR(50),
  [Well rna_id] NVARCHAR(50),
  [Well lab_id] NVARCHAR(50),
  [Well lh_sample_uuid] NVARCHAR(50),
);
