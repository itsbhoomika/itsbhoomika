USE clearledger;
-- DML 51: Edit a Transaction
-- Updates the amount and category of an existing transaction.
-- Transaction 9 (Thai Restaurant) is corrected: amount adjusted
-- and recategorized from Dining Out (category_id = 5) to Entertainment (category_id = 7).

UPDATE transaction
SET
    amount      = 55.00,
    category_id = 7
WHERE
    transaction_id = 9
;
