USE clearledger;
-- DML 52: Delete a Transaction
-- Removes a transaction that was entered in error.
-- Deletes transaction 10 (Concert Tickets) for User 1 (Bhoomika).

DELETE FROM transaction
WHERE
    transaction_id = 10
;
