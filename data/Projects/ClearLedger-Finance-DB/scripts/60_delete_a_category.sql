USE clearledger;
-- DML 60: Delete a Category
-- Removes a category for User 1 (Bhoomika).
-- Child rows in transaction and budget that reference this category
-- must be deleted first to satisfy foreign key constraints.
-- Here, the 'Clothing' category added in script 59 is removed.
-- Since no transactions or budgets have been recorded against it,
-- only the category row itself is deleted.

DELETE FROM transaction
WHERE
    category_id = (
        SELECT category_id
        FROM   category
        WHERE  category_name = 'Clothing'
          AND  user_id = 1
    )
;

DELETE FROM budget
WHERE
    category_id = (
        SELECT category_id
        FROM   category
        WHERE  category_name = 'Clothing'
          AND  user_id = 1
    )
;

DELETE FROM category
WHERE
    category_name = 'Clothing'
    AND user_id = 1
;
