delete from CherrypickingInfo;

INSERT INTO CherrypickingInfo
VALUES
  (1, 'TARGET1234', 'A01', 'SOURCE1234', 'B01', '2020-11-01 14:30:01', '1.0.0', '2020-11-01 21:30:01'),
  (1, 'TARGET1234', 'A01', 'SOURCE1234', 'B01', '2020-11-01 14:30:01', '1.0.0', '2020-11-01 21:30:01'),
  (1, 'TARGET1234', 'A01', 'SOURCE1234', 'B01', '2020-11-01 14:30:01', '1.0.0', '2020-11-01 21:30:01');

-- Query all properties for labware ()
-- select * from labwareprops 
-- inner join labware on labware.lab_pk=labwareprops.lab_fk 
-- inner join runs on runs.run_pk=labware.run_fk 
-- inner join wells on wells.lab_fk=labware.lab_pk
-- inner join wellprops on wellprops.well_fk=wells.well_pk
-- where labp_name='LIMS BARCODE' and labp_value='AP-rna-00148440';
