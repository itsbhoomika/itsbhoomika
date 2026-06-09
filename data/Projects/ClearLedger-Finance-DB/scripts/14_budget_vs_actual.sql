USE clearledger;
-- Query 14: Budget vs. Actual Spending
-- Compares each user's monthly budget limit per category against what
-- was actually spent that month. Flags over-budget and near-limit categories.

SELECT
    CONCAT(u.first_name, ' ', u.last_name)          AS user_name,
    c.category_name,
    b.month,
    b.year,
    b.monthly_limit,
    COALESCE(SUM(t.amount), 0.00)                    AS actual_spent,
    b.monthly_limit - COALESCE(SUM(t.amount), 0.00) AS remaining,
    CASE
        WHEN COALESCE(SUM(t.amount), 0.00) > b.monthly_limit            THEN 'OVER BUDGET'
        WHEN COALESCE(SUM(t.amount), 0.00) >= b.monthly_limit * 0.90   THEN 'Near Limit'
        ELSE 'On Track'
    END AS budget_status
FROM
    budget b
        JOIN user u         USING (user_id)
        JOIN category c     USING (category_id)
        LEFT JOIN transaction t
            ON  t.category_id             = b.category_id
            AND MONTH(t.transaction_date) = b.month
            AND YEAR(t.transaction_date)  = b.year
            AND t.transaction_type_id     = (
                    SELECT transaction_type_id
                    FROM   transaction_type_lookup
                    WHERE  transaction_type_name = 'Expense'
                )
GROUP BY
    b.budget_id
ORDER BY
    user_name,
    b.year,
    b.month,
    budget_status,
    c.category_name
;
