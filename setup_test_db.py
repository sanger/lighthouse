# flake8: noqa
import lighthouse.config.test as config  # type: ignore
from lighthouse.helpers.mysql_db import create_mysql_connection_engine

# Set up a basic MLWH db for testing
"""Drop and recreate required tables."""
print("Initialising the test MySQL MLWH database")

sql_engine = create_mysql_connection_engine(config.WAREHOUSES_RW_CONN_STRING)

create_db = """
CREATE DATABASE IF NOT EXISTS `unified_warehouse_test` /*!40100 DEFAULT CHARACTER SET latin1 */;
"""
drop_table_lh_sample = """
DROP TABLE IF EXISTS `unified_warehouse_test`.`lighthouse_sample`;
"""

drop_table_sample = """
DROP TABLE IF EXISTS `unified_warehouse_test`.`sample`;
"""

drop_table_stock_resource = """
DROP TABLE IF EXISTS `unified_warehouse_test`.`stock_resource`;
"""

drop_table_study = """
DROP TABLE IF EXISTS `unified_warehouse_test`.`study`;
"""

create_table_lh_sample = """
CREATE TABLE `unified_warehouse_test`.`lighthouse_sample` (
`id` int NOT NULL AUTO_INCREMENT,
`mongodb_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Auto-generated id from MongoDB',
`root_sample_id` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Id for this sample provided by the Lighthouse lab',
`cog_uk_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Consortium-wide id, generated by Sanger on import to LIMS',
`rna_id` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Lighthouse lab-provided id made up of plate barcode and well',
`plate_barcode` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Barcode of plate sample arrived in, from rna_id',
`coordinate` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Well position from plate sample arrived in, from rna_id',
`result` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Covid-19 test result from the Lighthouse lab',
`date_tested_string` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'When the covid-19 test was carried out by the Lighthouse lab',
`date_tested` datetime DEFAULT NULL COMMENT 'date_tested_string in date format',
`source` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Lighthouse centre that the sample came from',
`lab_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Id of the lab, within the Lighthouse centre',
`lh_sample_uuid` varchar(36) DEFAULT NULL COMMENT 'Lighthouse sample unique identifier',
`lh_source_plate_uuid` varchar(36) DEFAULT NULL COMMENT 'Lighthouse source plate unique identifier',
`created_at` datetime DEFAULT NULL COMMENT 'When this record was inserted',
`updated_at` datetime DEFAULT NULL COMMENT 'When this record was last updated',
PRIMARY KEY (`id`),
UNIQUE KEY `index_lighthouse_sample_on_root_sample_id_and_rna_id_and_result` (`root_sample_id`,`rna_id`,`result`),
UNIQUE KEY `index_lighthouse_sample_on_mongodb_id` (`mongodb_id`),
UNIQUE KEY `index_lighthouse_sample_on_lh_sample_uuid` (`lh_sample_uuid`),
KEY `index_lighthouse_sample_on_date_tested` (`date_tested`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

create_table_sample = """
CREATE TABLE `unified_warehouse_test`.`sample` (
  `id_sample_tmp` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Internal to this database id, value can change',
  `id_lims` varchar(10) COLLATE utf8_unicode_ci NOT NULL COMMENT 'LIM system identifier, e.g. CLARITY-GCLP, SEQSCAPE',
  `uuid_sample_lims` varchar(36) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'LIMS-specific sample uuid',
  `id_sample_lims` varchar(20) COLLATE utf8_unicode_ci NOT NULL COMMENT 'LIMS-specific sample identifier',
  `last_updated` datetime NOT NULL COMMENT 'Timestamp of last update',
  `recorded_at` datetime NOT NULL COMMENT 'Timestamp of warehouse update',
  `deleted_at` datetime DEFAULT NULL COMMENT 'Timestamp of sample deletion',
  `created` datetime DEFAULT NULL COMMENT 'Timestamp of sample creation',
  `name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `reference_genome` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `organism` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `accession_number` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `common_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8_unicode_ci,
  `taxon_id` int(6) unsigned DEFAULT NULL,
  `father` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `mother` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `replicate` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ethnicity` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `gender` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `cohort` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `country_of_origin` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `geographical_region` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sanger_sample_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `control` tinyint(1) DEFAULT NULL,
  `supplier_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `public_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sample_visibility` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `strain` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `consent_withdrawn` tinyint(1) NOT NULL DEFAULT '0',
  `donor_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phenotype` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'The phenotype of the sample as described in Sequencescape',
  `developmental_stage` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Developmental Stage',
  `control_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_sample_tmp`),
  UNIQUE KEY `index_sample_on_id_sample_lims_and_id_lims` (`id_sample_lims`,`id_lims`),
  UNIQUE KEY `sample_uuid_sample_lims_index` (`uuid_sample_lims`),
  KEY `sample_accession_number_index` (`accession_number`),
  KEY `sample_name_index` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4925703 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

create_table_stock_resource = """
CREATE TABLE `unified_warehouse_test`.`stock_resource` (
  `id_stock_resource_tmp` int(11) NOT NULL AUTO_INCREMENT,
  `last_updated` datetime NOT NULL COMMENT 'Timestamp of last update',
  `recorded_at` datetime NOT NULL COMMENT 'Timestamp of warehouse update',
  `created` datetime NOT NULL COMMENT 'Timestamp of initial registration of stock in LIMS',
  `deleted_at` datetime DEFAULT NULL COMMENT 'Timestamp of initial registration of deletion in parent LIMS. NULL if not deleted.',
  `id_sample_tmp` int(10) unsigned NOT NULL COMMENT 'Sample id, see "sample.id_sample_tmp"',
  `id_study_tmp` int(10) unsigned NOT NULL COMMENT 'Sample id, see "study.id_study_tmp"',
  `id_lims` varchar(10) COLLATE utf8_unicode_ci NOT NULL COMMENT 'LIM system identifier',
  `id_stock_resource_lims` varchar(20) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Lims specific identifier for the stock',
  `stock_resource_uuid` varchar(36) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Uuid identifier for the stock',
  `labware_type` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'The type of labware containing the stock. eg. Well, Tube',
  `labware_machine_barcode` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'The barcode of the containing labware as read by a barcode scanner',
  `labware_human_barcode` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'The barcode of the containing labware in human readable format',
  `labware_coordinate` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'For wells, the coordinate on the containing plate. Null for tubes.',
  `current_volume` float DEFAULT NULL COMMENT 'The current volume of material in microlitres based on measurements and know usage',
  `initial_volume` float DEFAULT NULL COMMENT 'The result of the initial volume measurement in microlitres conducted on the material',
  `concentration` float DEFAULT NULL COMMENT 'The concentration of material recorded in the lab in nanograms per microlitre',
  `gel_pass` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'The recorded result for the qel QC assay.',
  `pico_pass` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'The recorded result for the pico green assay. A pass indicates a successful assay, not sufficient material.',
  `snp_count` int(11) DEFAULT NULL COMMENT 'The number of markers detected in genotyping assays',
  `measured_gender` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'The gender call base on the genotyping assay',
  PRIMARY KEY (`id_stock_resource_tmp`),
  KEY `fk_stock_resource_to_sample` (`id_sample_tmp`),
  KEY `fk_stock_resource_to_study` (`id_study_tmp`),
  KEY `composition_lookup_index` (`id_stock_resource_lims`,`id_sample_tmp`,`id_lims`),
  CONSTRAINT `fk_stock_resource_to_sample` FOREIGN KEY (`id_sample_tmp`) REFERENCES `sample` (`id_sample_tmp`),
  CONSTRAINT `fk_stock_resource_to_study` FOREIGN KEY (`id_study_tmp`) REFERENCES `study` (`id_study_tmp`)
) ENGINE=InnoDB AUTO_INCREMENT=4656364 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

create_table_study = """
CREATE TABLE `unified_warehouse_test`.`study` (
  `id_study_tmp` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Internal to this database id, value can change',
  `id_lims` varchar(10) COLLATE utf8_unicode_ci NOT NULL COMMENT 'LIM system identifier, e.g. GCLP-CLARITY, SEQSCAPE',
  `uuid_study_lims` varchar(36) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'LIMS-specific study uuid',
  `id_study_lims` varchar(20) COLLATE utf8_unicode_ci NOT NULL COMMENT 'LIMS-specific study identifier',
  `last_updated` datetime NOT NULL COMMENT 'Timestamp of last update',
  `recorded_at` datetime NOT NULL COMMENT 'Timestamp of warehouse update',
  `deleted_at` datetime DEFAULT NULL COMMENT 'Timestamp of study deletion',
  `created` datetime DEFAULT NULL COMMENT 'Timestamp of study creation',
  `name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `reference_genome` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ethically_approved` tinyint(1) DEFAULT NULL,
  `faculty_sponsor` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `state` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `study_type` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `abstract` text COLLATE utf8_unicode_ci,
  `abbreviation` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `accession_number` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8_unicode_ci,
  `contains_human_dna` tinyint(1) DEFAULT NULL COMMENT 'Lane may contain human DNA',
  `contaminated_human_dna` tinyint(1) DEFAULT NULL COMMENT 'Human DNA in the lane is a contaminant and should be removed',
  `data_release_strategy` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `data_release_sort_of_study` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ena_project_id` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `study_title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `study_visibility` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ega_dac_accession_number` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `array_express_accession_number` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ega_policy_accession_number` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `data_release_timing` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `data_release_delay_period` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `data_release_delay_reason` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `remove_x_and_autosomes` tinyint(1) NOT NULL DEFAULT '0',
  `aligned` tinyint(1) NOT NULL DEFAULT '1',
  `separate_y_chromosome_data` tinyint(1) NOT NULL DEFAULT '0',
  `data_access_group` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `prelim_id` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'The preliminary study id prior to entry into the LIMS',
  `hmdmc_number` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'The Human Materials and Data Management Committee approval number(s) for the study.',
  `data_destination` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'The data destination type(s) for the study. It could be ''standard'', ''14mg'' or ''gseq''. This may be extended, if Sanger gains more external customers. It can contain multiply destinations separated by a space.',
  `s3_email_list` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `data_deletion_period` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_study_tmp`),
  UNIQUE KEY `study_id_lims_id_study_lims_index` (`id_lims`,`id_study_lims`),
  UNIQUE KEY `study_uuid_study_lims_index` (`uuid_study_lims`),
  KEY `study_accession_number_index` (`accession_number`),
  KEY `study_name_index` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6148 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

with sql_engine.connect() as connection:
    connection.execute(create_db)

    print("*** Dropping table LIGHTHOUSE SAMPLE ***")
    connection.execute(drop_table_lh_sample)
    print("*** Dropping table STOCK RESOURCE ***")
    connection.execute(drop_table_stock_resource)
    print("*** Dropping table STUDY ***")
    connection.execute(drop_table_study)
    print("*** Dropping table SAMPLE ***")
    connection.execute(drop_table_sample)

    print("*** Creating table SAMPLE ***")
    connection.execute(create_table_sample)
    print("*** Creating table STUDY ***")
    connection.execute(create_table_study)
    print("*** Creating table STOCK RESOURCE ***")
    connection.execute(create_table_stock_resource)
    print("*** Creating table LIGHTHOUSE SAMPLE ***")
    connection.execute(create_table_lh_sample)

print("Initialising the test MySQL events warehouse database")

create_db = """
CREATE DATABASE IF NOT EXISTS `event_warehouse_test` /*!40100 DEFAULT CHARACTER SET latin1 */;
"""
drop_table_subjects = """
DROP TABLE IF EXISTS `event_warehouse_test`.`subjects`;
"""

drop_table_roles = """
DROP TABLE IF EXISTS `event_warehouse_test`.`roles`;
"""

drop_table_events = """
DROP TABLE IF EXISTS `event_warehouse_test`.`events`;
"""

drop_table_event_types = """
DROP TABLE IF EXISTS `event_warehouse_test`.`event_types`;
"""

drop_table_subject_types = """
DROP TABLE IF EXISTS `event_warehouse_test`.`subject_types`;
"""

drop_table_role_types = """
DROP TABLE IF EXISTS `event_warehouse_test`.`role_types`;
"""

create_table_subjects = """
CREATE TABLE `event_warehouse_test`.`subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` binary(16) NOT NULL COMMENT 'A binary encoded UUID use HEX(uuid) to retrieve the original (minus dashes)',
  `friendly_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'A user readable identifier for the subject',
  `subject_type_id` int(11) NOT NULL COMMENT 'References the event type',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_subjects_on_uuid` (`uuid`) USING BTREE,
  KEY `index_subjects_on_friendly_name` (`friendly_name`) USING BTREE,
  KEY `fk_rails_b7f2e355a0` (`subject_type_id`) USING BTREE,
  CONSTRAINT `fk_rails_b7f2e355a0` FOREIGN KEY (`subject_type_id`) REFERENCES `subject_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4198465 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

create_table_roles = """
CREATE TABLE `event_warehouse_test`.`roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL COMMENT 'Associate with the event (what happened)',
  `subject_id` int(11) NOT NULL COMMENT 'Associate with the subject (what it happened to, or what might care)',
  `role_type_id` int(11) NOT NULL COMMENT 'References the role_types table, describing the role',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_roles_on_event_id` (`event_id`) USING BTREE,
  KEY `fk_rails_df614e5484` (`role_type_id`) USING BTREE,
  KEY `index_roles_on_subject_id` (`subject_id`) USING BTREE,
  CONSTRAINT `fk_rails_42eade4dd3` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`),
  CONSTRAINT `fk_rails_df614e5484` FOREIGN KEY (`role_type_id`) REFERENCES `role_types` (`id`),
  CONSTRAINT `fk_rails_e0c7d3e302` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51090114 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

create_table_events = """
CREATE TABLE `event_warehouse_test`.`events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lims_id` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Identifier for the originating LIMS. eg. SQSCP for Sequencesacape',
  `uuid` binary(16) NOT NULL COMMENT 'A binary encoded UUID use HEX(uuid) to retrieve the original (minus dashes)',
  `event_type_id` int(11) NOT NULL COMMENT 'References the event type',
  `occured_at` datetime NOT NULL COMMENT 'The time at which the event was recorded as happening. Other timestamps record when the event entered the database',
  `user_identifier` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_events_on_uuid` (`uuid`) USING BTREE,
  KEY `fk_rails_75f14fef31` (`event_type_id`) USING BTREE,
  CONSTRAINT `fk_rails_75f14fef31` FOREIGN KEY (`event_type_id`) REFERENCES `event_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1268003 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

create_table_event_types = """
CREATE TABLE `event_warehouse_test`.`event_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'The identifier for the event',
  `description` text COLLATE utf8_unicode_ci NOT NULL COMMENT 'A description of the meaning of the event',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_event_types_on_key` (`key`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=51468 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

create_table_subject_types = """
CREATE TABLE `event_warehouse_test`.`subject_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'The identifier for the role type',
  `description` text COLLATE utf8_unicode_ci NOT NULL COMMENT 'A description of the subject type',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_subject_types_on_key` (`key`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

create_table_role_types = """
CREATE TABLE `event_warehouse_test`.`role_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT 'The identifier for the role type',
  `description` text COLLATE utf8_unicode_ci NOT NULL COMMENT 'A description of the role',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_role_types_on_key` (`key`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
"""

with sql_engine.connect() as connection:
    connection.execute(create_db)

    print("*** Dropping table ROLES ***")
    connection.execute(drop_table_roles)
    print("*** Dropping table ROLE TYPES ***")
    connection.execute(drop_table_role_types)
    print("*** Dropping table EVENTS ***")
    connection.execute(drop_table_events)
    print("*** Dropping table EVENT TYPES ***")
    connection.execute(drop_table_event_types)
    print("*** Dropping table SUBJECT ***")
    connection.execute(drop_table_subjects)
    print("*** Dropping table SUBJECT TYPES ***")
    connection.execute(drop_table_subject_types)

    print("*** Creating table SUBJECT TYPES ***")
    connection.execute(create_table_subject_types)
    print("*** Creating table SUBJECTS ***")
    connection.execute(create_table_subjects)
    print("*** Creating table EVENT TYPES ***")
    connection.execute(create_table_event_types)
    print("*** Creating table EVENTS ***")
    connection.execute(create_table_events)
    print("*** Creating table ROLE TYPES ***")
    connection.execute(create_table_role_types)
    print("*** Creating table ROLES ***")
    connection.execute(create_table_roles)

print("Done")
