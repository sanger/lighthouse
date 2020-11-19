delete from CherrypickingInfo;

INSERT INTO CherrypickingInfo
VALUES
  (1, 'test1', 'A01', '123', 'A01', NULL, 'MCM001', 'rna_1', 'Lab 1', '8000a18d-43c6-44ff-9adb-257cb812ac77'),
  (2, 'test1', 'B01', '456', 'A01', NULL, 'MCM002', 'rna_2', 'Lab 2', '2f695461-4598-4dc1-8e80-b68c728be717'),
  (2, 'test1', 'C01', '789', 'B01', 'positive', NULL, NULL, NULL, NULL),
  (3, 'test1', 'C01', '789', 'C01', NULL, NULL, NULL, NULL, NULL);
