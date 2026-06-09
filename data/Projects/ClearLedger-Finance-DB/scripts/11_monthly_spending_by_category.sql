USE clearledger;
-- Query 11: Monthly Spending by Category
-- For each user, shows total spent per expense category per month,
-- ordered chronologically. Useful for identifying spending trends over time.

SELECT
    CONCAT(u.first_name, ' ', u.last_name) AS user_name,
    YEAR(t.transaction_date)               AS year,
    MONTH(t.transaction_date)              AS month,
    c.category_name,
    COUNT(t.transaction_id)                AS transaction_count,
    SUM(t.amount)                          AS total_spent
FROM
    user u
        JOIN account a                   USING (user_id)
        JOIN transaction t               USING (account_id)
        JOIN category c                  ON  t.category_id = c.category_id
        JOIN transaction_type_lookup ttl ON  t.transaction_type_id = ttl.transaction_type_id
WHERE
    ttl.transaction_type_name = 'Expense'
GROUP BY
    u.user_id,
    YEAR(t.transaction_date),
    MONTH(t.transaction_date),
    c.category_id
ORDER BY
    user_name,
    year,
    month,
    total_spent DESC
;
