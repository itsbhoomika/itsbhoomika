USE clearledger;
-- DML 55: Add a New Monthly Budget
-- Creates a new monthly budget for User 1 (Bhoomika) for a category
-- that did not previously have a budget set (Freelance income tracking
-- is not needed, so we add a Dining Out budget for May 2024).
-- The category (category_id = 5, Dining Out) already exists for this user.

INSERT INTO budget
    VALUES (DEFAULT, 200.00, 5, 2024, 1, 5);
