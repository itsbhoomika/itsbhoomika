USE clearledger;
-- Query 13: Account Balance and Activity Summary
-- For each account, shows the owner, account type, current balance,
-- total income deposited, total expenses charged, and transaction count.
-- Gives users a complete picture of each account's activity in one report.

SELECT
    CONCAT(u.first_name, ' ', u.last_name)                                                   AS user_name,
    a.account_name,
    atl.account_type_name                                                                     AS account_type,
    a.opened_date,
    a.current_balance,
    COALESCE(SUM(CASE WHEN ttl.transaction_type_name = 'Income'  THEN t.amount END), 0.00)  AS total_income_recorded,
    COALESCE(SUM(CASE WHEN ttl.transaction_type_name = 'Expense' THEN t.amount END), 0.00)  AS total_expenses_recorded,
    COUNT(t.transaction_id)                                                                   AS transaction_count
FROM
    user u
        JOIN account a                        USING (user_id)
        JOIN account_type_lookup atl          ON  a.account_type_id = atl.account_type_id
        LEFT JOIN transaction t               USING (account_id)
        LEFT JOIN transaction_type_lookup ttl ON  t.transaction_type_id = ttl.transaction_type_id
GROUP BY
    a.account_id
ORDER BY
    user_name,
    atl.account_type_name,
    a.account_name
;
