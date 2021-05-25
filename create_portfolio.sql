CREATE TABLE transactions(
	`owner` VARCHAR(100) NOT NULL,
	`originalprice` float(10,2) NOT NULL,
	`quantity` int(11) NOT NULL DEFAULT 1,
	`purchase_date` timestamp NOT NULL DEFAULT current_timestamp()
);
