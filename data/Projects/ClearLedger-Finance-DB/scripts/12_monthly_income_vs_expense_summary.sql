USE clearledger;
-- Query 12: Monthly Income vs. Expense Summary
-- For each user, summarizes total income, total expenses, and net cash flow
-- per month across all accounts. This is a key summary report that lets users
-- see at a glance whether they are spending more or less than they earn.

SELECT
    CONCAT(u.first_name, ' ', u.last_name)                                                    AS user_name,
    YEAR(t.transaction_date)                                                                   AS year,
    MONTH(t.transaction_date)                                                                  AS month,
    COALESCE(SUM(CASE WHEN ttl.transaction_type_name = 'Income'  THEN t.amount END), 0.00)   AS total_income,
    COALESCE(SUM(CASE WHEN ttl.transaction_type_name = 'Expense' THEN t.amount END), 0.00)   AS total_expenses,
    COALESCE(SUM(CASE WHEN ttl.transaction_type_name = 'Income'  THEN t.amount END), 0.00)
        - COALESCE(SUM(CASE WHEN ttl.transaction_type_name = 'Expense' THEN t.amount END), 0.00) AS net_cash_flow
FROM
    user u
        JOIN account a                   USING (user_id)
        JOIN transaction t               USING (account_id)
        JOIN transaction_type_lookup ttl ON  t.transaction_type_id = ttl.transaction_type_id
GROUP BY
    u.user_id,
    YEAR(t.transaction_date),
    MONTH(t.transaction_date)
ORDER BY
    user_name,
    year,
    month
;
