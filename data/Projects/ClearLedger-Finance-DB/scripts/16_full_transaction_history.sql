USE clearledger;
-- Query 16: Full Transaction History Per Account
-- A complete ledger view per account showing every transaction in
-- chronological order with account type, transaction type, and category label.
-- Useful as a printable account statement.

SELECT
    CONCAT(u.first_name, ' ', u.last_name) AS user_name,
    a.account_name,
    atl.account_type_name                  AS account_type,
    t.transaction_date,
    ttl.transaction_type_name              AS transaction_type,
    c.category_name,
    t.description,
    t.amount
FROM
    user u
        JOIN account a                   USING (user_id)
        JOIN account_type_lookup atl     ON  a.account_type_id = atl.account_type_id
        JOIN transaction t               USING (account_id)
        JOIN transaction_type_lookup ttl ON  t.transaction_type_id = ttl.transaction_type_id
        JOIN category c                  ON  t.category_id = c.category_id
ORDER BY
    user_name,
    a.account_name,
    t.transaction_date,
    t.transaction_id
;
