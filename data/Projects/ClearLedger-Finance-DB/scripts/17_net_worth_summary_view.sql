USE clearledger;
-- Query 17: Net Worth Summary View
-- Creates a reusable view that shows each user's total income recorded,
-- total expenses recorded, net cash flow, and total balance across all accounts.
-- This is the highest-level financial health snapshot in the system.

CREATE OR REPLACE VIEW net_worth_summary_view AS
    SELECT
        u.user_id,
        CONCAT(u.first_name, ' ', u.last_name)                                                    AS user_name,
        COALESCE(SUM(CASE WHEN ttl.transaction_type_name = 'Income'  THEN t.amount END), 0.00)   AS total_income,
        COALESCE(SUM(CASE WHEN ttl.transaction_type_name = 'Expense' THEN t.amount END), 0.00)   AS total_expenses,
        COALESCE(SUM(CASE WHEN ttl.transaction_type_name = 'Income'  THEN t.amount END), 0.00)
            - COALESCE(SUM(CASE WHEN ttl.transaction_type_name = 'Expense' THEN t.amount END), 0.00) AS net_cash_flow,
        (SELECT SUM(a2.current_balance)
         FROM   account a2
         WHERE  a2.user_id = u.user_id)                                                            AS total_account_balance
    FROM
        user u
            LEFT JOIN account a                   USING (user_id)
            LEFT JOIN transaction t               USING (account_id)
            LEFT JOIN transaction_type_lookup ttl ON  t.transaction_type_id = ttl.transaction_type_id
    GROUP BY
        u.user_id
;

SELECT
    *
FROM
    net_worth_summary_view
ORDER BY
    user_id
;
