USE clearledger;
-- DML 57: Add a New Savings Goal
-- Creates a new savings goal for User 1 (Bhoomika).
-- goal_status_id = 1 (Active)

INSERT INTO savings_goal
    VALUES (DEFAULT, 'Graduate School Fund', 10000.00, 500.00, '2026-08-01', 1, 1);
