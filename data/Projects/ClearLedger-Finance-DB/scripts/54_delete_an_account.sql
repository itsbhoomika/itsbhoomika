USE clearledger;
-- DML 54: Delete an Account
-- Removes an account and all transactions associated with it.
-- Transactions must be deleted first to satisfy the foreign key constraint.
-- Here, account 6 (Discover Credit, User 2) is being closed and removed.

DELETE FROM transaction
WHERE
    account_id = 6;

DELETE FROM account
WHERE
    account_id = 6;
