USE clearledger;
-- DML 50: Add a New Transaction
-- Records a new expense transaction for User 1 (Bhoomika)
-- charged to her credit account (account_id = 3) under Groceries (category_id = 3).
-- transaction_type_id = 2 (Expense)

INSERT INTO transaction
    VALUES (DEFAULT, 78.50, '2024-04-25', 'Target Shopping Run', 2, 3, 3);
