CREATE TABLE transactions(
	`owner` VARCHAR(100) NOT NULL,
	`originalprice` float(10,2) NOT NULL,
	`quantity` int(11) NOT NULL DEFAULT 1,
	`total_price` float(10, 2) NOT NULL,
	`symbol` VARCHAR(10) NOT NULL,
	`purchase_date` timestamp NOT NULL DEFAULT current_timestamp()
);


CREATE TABLE history(
	`user` VARCHAR(100) NOT NULL,
	`symbol` VARCHAR(10) NOT NULL,
	`quantity` int(11) NOT NULL DEFAULT 1,
	`sell_price` float(10, 2) NOT NULL, 
	`earnings` float(10, 2) NOT NULL,
	`bought_price` float(10,2) NOT NULL,
	`date` timestamp NOT NULL DEFAULT current_timestamp()
);

ALTER TABLE users ADD positive_transactions int(10) NOT NULL DEFAULT 0;
ALTER TABLE users ADD negative_transactions int(10) NOT NULL DEFAULT 0;



-- Delete from owner and purchase_date