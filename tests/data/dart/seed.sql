delete from CherrypickingInfo;

INSERT INTO CherrypickingInfo
VALUES
-- dart_run_id int,
--    |destination_barcode NVARCHAR(50),
--    |              |destination_coordinate NVARCHAR(50),
--    |              |      |source_barcode NVARCHAR(50),
--    |              |      |             |source_coordinate NVARCHAR(50),
--    |              |      |             |      |control NVARCHAR(50),
--    |              |      |             |      |           |root_sample_id NVARCHAR(50),
--    |              |      |             |      |           |            |rna_id NVARCHAR(50),
--    |              |      |             |      |           |            |        |lab_id NVARCHAR(50),
  (2, 'des_plate_z', 'xxx', 'ignored',    'yyy', NULL,       'xyz',       'abcde', '12345', 'plate_1'), -- going to be ignored because we get the latest run
  (3, 'des_plate_1', 'A01', 'plate_123',  'A01', NULL,       'sample_001','rna_1', 'lab_1', 'plate_2'),
  (3, 'des_plate_1', 'A02', 'plate_123',  'A02', NULL,       'sample_002','rna_2', 'lab_1', 'plate_3'),
  (3, 'des_plate_1', 'A03', 'plate_456',  'A01', NULL,       'sample_003','rna_3', 'lab_2', 'plate_4'),
  (3, 'des_plate_1', 'A04', 'plate_789',  'A01', NULL,       'sample_004','rna_4', 'lab_2', 'plate_5'),
  (3, 'des_plate_1', 'A05', 'c_plate_1',  'C03', 'positive', NULL,        NULL,    NULL, 'plate_6'),
  (3, 'des_plate_1', 'A06', 'plate_abc',  'A01', NULL,       'sample_005','rna_5', 'lab_3', 'plate_7');
