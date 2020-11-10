delete from CherrypickingInfo;

INSERT INTO CherrypickingInfo
VALUES
  (1, 'plate_1', 'A01', '123', 'A01', '', 'MCM001', 'rna_1', 'Lab 1'),
  (2, 'plate_1', 'B01', '123', 'F01', '', 'MCM006', 'rna_1', 'Lab 1'),
  (2, 'plate_1', 'C01', '789', 'B01', 'positive', '', '', '');
-- Query all properties for labware ()
-- select * from labwareprops 
-- inner join labware on labware.lab_pk=labwareprops.lab_fk 
-- inner join runs on runs.run_pk=labware.run_fk 
-- inner join wells on wells.lab_fk=labware.lab_pk
-- inner join wellprops on wellprops.well_fk=wells.well_pk
-- where labp_name='LIMS BARCODE' and labp_value='AP-rna-00148440';
