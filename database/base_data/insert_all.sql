USE inithub;

UPDATE `django_site` SET `domain`='inithub.com', `name`='InitHub' WHERE `id`='1';

INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (1,'Mobile Technology','2012-07-31 17:50:07','2012-07-31 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (2,'Web Technology','2012-07-31 17:50:58','2012-07-31 17:50:58');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (3,'Retail','2013-08-06 17:50:07','2013-08-06 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (4,'Cloud Technology','2013-08-06 17:50:07','2013-08-06 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (5,'Manufacturing','2013-08-06 17:50:07','2013-08-06 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (6,'Marketing','2013-08-06 17:50:07','2013-08-06 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (7,'Environment','2013-08-06 17:50:07','2013-08-06 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (8,'Social Media','2013-08-06 17:50:07','2013-08-06 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (9,'Recreation','2013-08-06 17:50:07','2013-08-06 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (10,'Software','2013-08-06 17:50:07','2013-08-06 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (11,'Consumer Electronics','2013-08-06 17:50:07','2013-08-06 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (12,'Transportation','2013-08-06 17:50:07','2013-08-06 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (13,'Health','2013-08-06 17:50:07','2013-08-06 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (14,'Education','2013-08-06 17:50:07','2013-08-06 17:50:07');
INSERT INTO `manager_interest` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (15,'Fitness','2013-08-06 17:50:07','2013-08-06 17:50:07');

INSERT INTO `manager_milestone` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (1,'Incorporate','2012-08-02 22:12:17','2012-08-02 22:12:17');
INSERT INTO `manager_milestone` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (2,'Develop Prototype','2012-08-02 22:13:21','2012-09-22 14:28:59');
INSERT INTO `manager_milestone` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (3,'Mobile Application','2012-09-22 14:28:04','2012-09-22 14:28:04');
INSERT INTO `manager_milestone` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (4,'Raise Money','2012-09-22 14:28:15','2012-09-22 14:28:15');
INSERT INTO `manager_milestone` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (5,'Fist Paying Customer','2012-09-22 14:29:16','2012-09-22 14:29:16');
INSERT INTO `manager_milestone` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (6,'Social Media Presence','2012-09-22 14:29:50','2012-09-22 14:29:50');
INSERT INTO `manager_milestone` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (7,'Profitable','2012-09-22 14:30:27','2012-09-22 14:30:27');
INSERT INTO `manager_milestone` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (8,'First Employee','2012-09-22 14:30:56','2012-09-22 14:30:56');
INSERT INTO `manager_milestone` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (9,'Assemble Core Team','2012-09-22 14:31:09','2012-09-22 14:31:09');
INSERT INTO `manager_milestone` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (10,'Launch Web Site','2012-09-22 14:31:30','2012-09-22 14:31:30');
INSERT INTO `manager_milestone` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (11,'Press/Blog Coverage','2012-09-22 14:32:15','2012-09-22 14:32:15');
INSERT INTO `manager_milestone` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (12,'Launch Crowdfunding Campaign','2013-10-25 14:32:15','2013-10-25 14:32:15');

INSERT INTO `manager_promotion` (`id`,`short_desc`,`long_desc`,`code`,`start_date`,`end_date`,`create_date`,`modified_date`) VALUES (1,'Solutiosoft Promo','default Solutiosoft promo','INNOHUB','2012-07-26 13:55:50','2015-07-26 13:55:50','2012-07-26 13:55:50','2012-07-26 13:55:50');
INSERT INTO `manager_promotion` (`id`,`short_desc`,`long_desc`,`code`,`start_date`,`end_date`,`create_date`,`modified_date`) VALUES (2,'User Invite','Existing user invitation','USER','2013-07-15 13:55:50','2050-07-15 13:55:50','2013-07-15 13:55:50','2013-07-15 13:55:50');

INSERT INTO `manager_service` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (1,'Mentor/Advisor','2012-07-25 12:28:56','2012-07-25 12:28:56');
INSERT INTO `manager_service` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (2,'Legal','2012-07-25 12:29:07','2012-07-25 12:29:07');
INSERT INTO `manager_service` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (3,'Accounting','2012-07-25 12:30:44','2012-07-25 12:30:44');
INSERT INTO `manager_service` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (4,'Marketing','2012-07-25 12:33:46','2012-07-25 12:33:46');
INSERT INTO `manager_service` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (5,'Design','2012-07-25 12:34:45','2012-07-25 12:34:45');
INSERT INTO `manager_service` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (6,'Development','2012-07-25 12:34:51','2012-07-25 12:34:51');
INSERT INTO `manager_service` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (7,'Customer Support','2012-09-22 14:27:01','2012-09-22 14:27:01');
INSERT INTO `manager_service` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (8,'Quality Assurance/Testing','2012-09-22 14:27:21','2012-09-22 14:27:21');
INSERT INTO `manager_service` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (9,'Operations/System Admin','2012-09-22 14:33:15','2012-09-22 14:33:15');

INSERT INTO `manager_subscription` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (1,'InitHub Updates','2012-10-30 21:17:35','2012-10-30 21:17:35');

INSERT INTO `support_item_type` (`id`,`short_desc`,`create_date`,`modified_date`) VALUES (1,'Internal','2012-09-05 22:05:12','2013-01-12 08:05:12');
