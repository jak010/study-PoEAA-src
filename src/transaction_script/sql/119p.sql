CREATE TABLE products (
	id int(1) PRIMARY KEY,
	name VARCHAR(255),
	`type` VARCHAR(64)	
) Engine=innodb;


CREATE TABLE contracts (
	id int(1) PRIMARY KEY,
	product int(1),
	revenue decimal(65,0),
	dateSigned date
) Engine=innodb;


CREATE TABLE revenueRecognitions(
	contract int(1),
	amount decimal(65,0),
	recognizedOn date,
	PRIMARY KEY(contract, recognizedOn)
) Engine=innodb;


INSERT INTO pofeaa.products (id, name, `type`) VALUES(1, 'mysql', 'D');
INSERT INTO pofeaa.products (id, name, `type`) VALUES(2, 'spreadsheet', 'S');
INSERT INTO pofeaa.products (id, name, `type`) VALUES(3, 'wordprocessor', 'W');

INSERT INTO pofeaa.contracts (id, product, revenue, dateSigned) VALUES(1, 1, 100, now());
INSERT INTO pofeaa.contracts (id, product, revenue, dateSigned) VALUES(2, 2, 200, now());
INSERT INTO pofeaa.contracts (id, product, revenue, dateSigned) VALUES(3, 3, 300, now());