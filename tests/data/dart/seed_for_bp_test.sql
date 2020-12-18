delete from CherrypickingInfo;

INSERT INTO CherrypickingInfo
VALUES
  (1, 'plate_1', 'D01', 'this_line_will_be_ignored', 'A01', NULL, 'MCM007', 'rna_1', 'Lab 1'),
  (2, 'plate_1', 'A01', '123', 'A01', NULL, 'MCM001', 'rna_1', 'Lab 1'),
  (2, 'plate_1', 'B01', '123', 'F01', NULL, 'MCM006', 'rna_1', 'Lab 1'),
  (2, 'plate_1', 'C01', '789', 'B01', 'positive', NULL, NULL, NULL);
