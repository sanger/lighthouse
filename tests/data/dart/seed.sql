delete from CherrypickingInfo;

INSERT INTO CherrypickingInfo
VALUES
  ('test1', 0, '123', 0, '', 'MCM001', 'rna_1', 'Lab 1'),
  ('test1', 1, '456', 0, '', 'MCM002', 'rna_2', 'Lab 2'),
  ('test1', 2, '789', 1, 'positive', '', '', '');
-- Query all properties for labware ()
-- select * from labwareprops 
-- inner join labware on labware.lab_pk=labwareprops.lab_fk 
-- inner join runs on runs.run_pk=labware.run_fk 
-- inner join wells on wells.lab_fk=labware.lab_pk
-- inner join wellprops on wellprops.well_fk=wells.well_pk
-- where labp_name='LIMS BARCODE' and labp_value='AP-rna-00148440';
