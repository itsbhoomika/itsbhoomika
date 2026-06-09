USE clearledger;
-- DML 56: Update an Existing Budget Limit
-- Adjusts the monthly limit for budget_id = 1 (User 1's Groceries budget
-- for April 2024) from $500.00 to $450.00 after a spending review.

UPDATE budget
SET
    monthly_limit = 450.00
WHERE
    budget_id = 1
;
