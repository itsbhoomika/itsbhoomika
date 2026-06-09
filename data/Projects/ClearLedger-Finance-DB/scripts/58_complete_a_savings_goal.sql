USE clearledger;
-- DML 58: Mark a Savings Goal as Completed
-- Updates a savings goal's status to 'Completed' and sets the
-- current_amount equal to the target once the user has reached their goal.
-- goal_status_id = 2 (Completed)
-- Here, goal 1 (Emergency Fund) for User 1 (Bhoomika) is marked complete.

UPDATE savings_goal
SET
    current_amount = target_amount,
    goal_status_id = 2
WHERE
    goal_id = 1
;
