USE clearledger;
-- Query 15: Savings Goals Progress
-- Shows each user's savings goals with progress percentage, amount remaining,
-- and how many days until the target date.

SELECT
    CONCAT(u.first_name, ' ', u.last_name)                AS user_name,
    sg.goal_name,
    sg.target_amount,
    sg.current_amount,
    sg.target_amount - sg.current_amount                   AS amount_remaining,
    ROUND((sg.current_amount / sg.target_amount) * 100, 1) AS percent_complete,
    sg.target_date,
    DATEDIFF(sg.target_date, CURDATE())                    AS days_remaining,
    gsl.goal_status_name                                   AS status
FROM
    user u
        JOIN savings_goal sg        USING (user_id)
        JOIN goal_status_lookup gsl ON  sg.goal_status_id = gsl.goal_status_id
ORDER BY
    user_name,
    gsl.goal_status_name,
    sg.target_date
;
