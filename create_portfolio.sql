CREATE TABLE transactions(
	`owner` VARCHAR(100) NOT NULL,
	`originalprice` float(10,2) NOT NULL,
	`quantity` int(11) NOT NULL DEFAULT 1,
	`total_price` float(10, 2) NOT NULL,
	`symbol` VARCHAR(10) NOT NULL,
	`purchase_date` timestamp NOT NULL DEFAULT current_timestamp()
);


-- Delete from owner and purchase_date