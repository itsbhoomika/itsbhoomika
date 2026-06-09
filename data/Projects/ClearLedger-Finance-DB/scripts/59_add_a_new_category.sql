USE clearledger;
-- DML 59: Add a New Category
-- Adds a new expense category 'Clothing' for User 1 (Bhoomika).
-- category_type_id = 2 (Expense)
-- The UNIQUE constraint on (category_name, user_id) prevents duplicate
-- category names for the same user.

INSERT INTO category
    VALUES (DEFAULT, 'Clothing', 2, 1);
