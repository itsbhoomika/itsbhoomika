USE clearledger;
-- DML 53: Add a New Account with Opening Deposit
-- Adds a new investment account for User 3 (Priya) and records the
-- opening deposit as an income transaction against it.
-- Requires inserting into both account and transaction (multi-table).
-- LAST_INSERT_ID() captures the AUTO_INCREMENT account_id assigned by the
-- first INSERT so the transaction row references the correct account.
-- account_type_id = 4 (Investment)
-- transaction_type_id = 1 (Income)

INSERT INTO account
    VALUES (DEFAULT, 'Ally Investment', 4, 5000.00, '2024-04-25', 3);

INSERT INTO transaction
    VALUES (DEFAULT, 5000.00, '2024-04-25', 'Opening Investment Deposit', 1, LAST_INSERT_ID(), 15);
