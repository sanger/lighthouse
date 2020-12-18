delete from CherrypickingInfo;

INSERT INTO CherrypickingInfo
VALUES
  (2, 'test1', 'A01', 'this_line_will_be_ignored', 'A01', NULL, 'MCM001', 'rna_1', 'Lab 1'),
  (3, 'test1', 'A01', '123', 'A01', NULL, 'MCM001', 'rna_1', 'Lab 1'),
  (3, 'test1', 'B01', '456', 'A01', NULL, 'MCM002', 'rna_2', 'Lab 2'),
  (3, 'test1', 'C01', '789', 'B01', 'positive', NULL, NULL, NULL),
  (3, 'test1', 'C01', '789', 'C01', NULL, NULL, NULL, NULL);
