DROP SCHEMA IF EXISTS `clearledger`;
CREATE SCHEMA IF NOT EXISTS `clearledger` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `clearledger`;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

--
-- Lookup table: account_type_lookup
--

DROP TABLE IF EXISTS `account_type_lookup`;
CREATE TABLE `account_type_lookup` (
  `account_type_id`   INT         NOT NULL AUTO_INCREMENT,
  `account_type_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`account_type_id`),
  UNIQUE KEY `account_type_name_UNIQUE` (`account_type_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `account_type_lookup` VALUES
  (1, 'Checking'),
  (2, 'Savings'),
  (3, 'Credit'),
  (4, 'Investment');

--
-- Lookup table: transaction_type_lookup
--

DROP TABLE IF EXISTS `transaction_type_lookup`;
CREATE TABLE `transaction_type_lookup` (
  `transaction_type_id`   INT         NOT NULL AUTO_INCREMENT,
  `transaction_type_name` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`transaction_type_id`),
  UNIQUE KEY `transaction_type_name_UNIQUE` (`transaction_type_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `transaction_type_lookup` VALUES
  (1, 'Income'),
  (2, 'Expense');

--
-- Lookup table: category_type_lookup
--

DROP TABLE IF EXISTS `category_type_lookup`;
CREATE TABLE `category_type_lookup` (
  `category_type_id`   INT         NOT NULL AUTO_INCREMENT,
  `category_type_name` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`category_type_id`),
  UNIQUE KEY `category_type_name_UNIQUE` (`category_type_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `category_type_lookup` VALUES
  (1, 'Income'),
  (2, 'Expense');

--
-- Lookup table: goal_status_lookup
--

DROP TABLE IF EXISTS `goal_status_lookup`;
CREATE TABLE `goal_status_lookup` (
  `goal_status_id`   INT         NOT NULL AUTO_INCREMENT,
  `goal_status_name` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`goal_status_id`),
  UNIQUE KEY `goal_status_name_UNIQUE` (`goal_status_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `goal_status_lookup` VALUES
  (1, 'Active'),
  (2, 'Completed'),
  (3, 'Cancelled');

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id`       INT           NOT NULL AUTO_INCREMENT,
  `first_name`    VARCHAR(45)   NOT NULL,
  `last_name`     VARCHAR(45)   NOT NULL,
  `email`         VARCHAR(100)  NOT NULL,
  `password_hash` VARCHAR(255)  NOT NULL,
  `created_at`    DATE          NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `user` VALUES
  (1, 'Bhoomika', 'Ravishankar', 'bhoomika@example.com', 'hashed_pw_1', '2024-01-15'),
  (2, 'Marcus',   'Rivera',      'marcus@example.com',   'hashed_pw_2', '2024-02-03'),
  (3, 'Priya',    'Nair',        'priya@example.com',    'hashed_pw_3', '2024-03-10');

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `account_id`      INT           NOT NULL AUTO_INCREMENT,
  `account_name`    VARCHAR(100)  NOT NULL,
  `account_type_id` INT           NOT NULL,
  `current_balance` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `opened_date`     DATE          NOT NULL,
  `user_id`         INT           NOT NULL,
  PRIMARY KEY (`account_id`),
  KEY `fk_account_user_idx`         (`user_id`),
  KEY `fk_account_account_type_idx` (`account_type_id`),
  CONSTRAINT `fk_account_user`         FOREIGN KEY (`user_id`)         REFERENCES `user`               (`user_id`),
  CONSTRAINT `fk_account_account_type` FOREIGN KEY (`account_type_id`) REFERENCES `account_type_lookup` (`account_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `account` VALUES
  -- account_type_id: 1=Checking, 2=Savings, 3=Credit, 4=Investment
  (1,  'Chase Checking',        1,  3240.50, '2022-08-01', 1),
  (2,  'Chase Savings',         2,  8500.00, '2022-08-01', 1),
  (3,  'Capital One Credit',    3,  -450.75, '2023-01-10', 1),
  (4,  'Wells Fargo Checking',  1,  1875.20, '2021-05-15', 2),
  (5,  'Wells Fargo Savings',   2,  4200.00, '2021-05-15', 2),
  (6,  'Discover Credit',       3,  -215.40, '2022-11-01', 2),
  (7,  'Ally Checking',         1,  2100.00, '2023-06-20', 3),
  (8,  'Ally Savings',          2,  6750.00, '2023-06-20', 3),
  (9,  'Citi Credit',           3,  -320.10, '2024-01-05', 3);

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `category_id`      INT          NOT NULL AUTO_INCREMENT,
  `category_name`    VARCHAR(100) NOT NULL,
  `category_type_id` INT          NOT NULL,
  `user_id`          INT          NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `uq_category_name_user` (`category_name`, `user_id`),
  KEY `fk_category_user_idx`          (`user_id`),
  KEY `fk_category_category_type_idx` (`category_type_id`),
  CONSTRAINT `fk_category_user`          FOREIGN KEY (`user_id`)          REFERENCES `user`                (`user_id`),
  CONSTRAINT `fk_category_category_type` FOREIGN KEY (`category_type_id`) REFERENCES `category_type_lookup` (`category_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `category` VALUES
  -- category_type_id: 1=Income, 2=Expense
  -- User 1 categories
  (1,  'Salary',         1, 1),
  (2,  'Freelance',      1, 1),
  (3,  'Groceries',      2, 1),
  (4,  'Rent',           2, 1),
  (5,  'Dining Out',     2, 1),
  (6,  'Utilities',      2, 1),
  (7,  'Entertainment',  2, 1),
  -- User 2 categories
  (8,  'Salary',         1, 2),
  (9,  'Side Income',    1, 2),
  (10, 'Groceries',      2, 2),
  (11, 'Rent',           2, 2),
  (12, 'Transportation', 2, 2),
  (13, 'Subscriptions',  2, 2),
  -- User 3 categories
  (14, 'Salary',         1, 3),
  (15, 'Investment',     1, 3),
  (16, 'Groceries',      2, 3),
  (17, 'Rent',           2, 3),
  (18, 'Healthcare',     2, 3),
  (19, 'Travel',         2, 3);

--
-- Table structure for table `budget`
--

DROP TABLE IF EXISTS `budget`;
CREATE TABLE `budget` (
  `budget_id`     INT           NOT NULL AUTO_INCREMENT,
  `monthly_limit` DECIMAL(10,2) NOT NULL,
  `month`         INT           NOT NULL COMMENT '1-12',
  `year`          INT           NOT NULL,
  `user_id`       INT           NOT NULL,
  `category_id`   INT           NOT NULL,
  PRIMARY KEY (`budget_id`),
  UNIQUE KEY `uq_budget_user_category_month_year` (`user_id`, `category_id`, `month`, `year`),
  KEY `fk_budget_user_idx`     (`user_id`),
  KEY `fk_budget_category_idx` (`category_id`),
  CONSTRAINT `fk_budget_user`     FOREIGN KEY (`user_id`)     REFERENCES `user`     (`user_id`),
  CONSTRAINT `fk_budget_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `budget` VALUES
  -- User 1 budgets (April 2024)
  (1,   500.00, 4, 2024, 1,  3),   -- Groceries
  (2,  1400.00, 4, 2024, 1,  4),   -- Rent
  (3,   150.00, 4, 2024, 1,  5),   -- Dining Out
  (4,   100.00, 4, 2024, 1,  6),   -- Utilities
  (5,    80.00, 4, 2024, 1,  7),   -- Entertainment
  -- User 2 budgets (April 2024)
  (6,   400.00, 4, 2024, 2, 10),   -- Groceries
  (7,  1200.00, 4, 2024, 2, 11),   -- Rent
  (8,   200.00, 4, 2024, 2, 12),   -- Transportation
  (9,    60.00, 4, 2024, 2, 13),   -- Subscriptions
  -- User 3 budgets (April 2024)
  (10,  450.00, 4, 2024, 3, 16),   -- Groceries
  (11, 1600.00, 4, 2024, 3, 17),   -- Rent
  (12,  200.00, 4, 2024, 3, 18),   -- Healthcare
  (13,  500.00, 4, 2024, 3, 19);   -- Travel

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
CREATE TABLE `transaction` (
  `transaction_id`      INT           NOT NULL AUTO_INCREMENT,
  `amount`              DECIMAL(10,2) NOT NULL,
  `transaction_date`    DATE          NOT NULL,
  `description`         VARCHAR(255)  DEFAULT NULL,
  `transaction_type_id` INT           NOT NULL,
  `account_id`          INT           NOT NULL,
  `category_id`         INT           NOT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `fk_transaction_account_idx`          (`account_id`),
  KEY `fk_transaction_category_idx`         (`category_id`),
  KEY `fk_transaction_transaction_type_idx` (`transaction_type_id`),
  CONSTRAINT `fk_transaction_account`          FOREIGN KEY (`account_id`)          REFERENCES `account`               (`account_id`),
  CONSTRAINT `fk_transaction_category`         FOREIGN KEY (`category_id`)         REFERENCES `category`              (`category_id`),
  CONSTRAINT `fk_transaction_transaction_type` FOREIGN KEY (`transaction_type_id`) REFERENCES `transaction_type_lookup` (`transaction_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `transaction` VALUES
  -- transaction_type_id: 1=Income, 2=Expense
  -- User 1 transactions (account 1=checking, account 3=credit)
  (1,  3200.00, '2024-04-01', 'April Salary Deposit',      1, 1, 1),
  (2,   450.00, '2024-04-03', 'Freelance Web Project',     1, 1, 2),
  (3,   112.50, '2024-04-05', 'Whole Foods Grocery Run',   2, 3, 3),
  (4,  1400.00, '2024-04-06', 'April Rent Payment',        2, 1, 4),
  (5,    45.00, '2024-04-08', 'Dinner at Olive Garden',    2, 3, 5),
  (6,    88.00, '2024-04-10', 'Electric & Internet Bill',  2, 1, 6),
  (7,    30.00, '2024-04-12', 'Movie Tickets',             2, 3, 7),
  (8,    95.20, '2024-04-15', 'Trader Joe\'s Grocery Run', 2, 3, 3),
  (9,    62.00, '2024-04-18', 'Thai Restaurant',           2, 3, 5),
  (10,   25.00, '2024-04-22', 'Concert Tickets',           2, 3, 7),
  -- User 2 transactions (account 4=checking, account 6=credit)
  (11, 2800.00, '2024-04-01', 'April Salary Deposit',      1, 4,  8),
  (12,  200.00, '2024-04-04', 'Dog Walking Side Income',   1, 4,  9),
  (13,   98.00, '2024-04-06', 'Aldi Grocery Run',          2, 6, 10),
  (14, 1200.00, '2024-04-07', 'April Rent Payment',        2, 4, 11),
  (15,   55.00, '2024-04-09', 'Monthly Bus Pass',          2, 4, 12),
  (16,   45.00, '2024-04-11', 'Netflix + Spotify',         2, 6, 13),
  (17,  110.00, '2024-04-14', 'Costco Grocery Run',        2, 6, 10),
  (18,   38.00, '2024-04-20', 'Lyft Rides',                2, 6, 12),
  -- User 3 transactions (account 7=checking, account 9=credit)
  (19, 4500.00, '2024-04-01', 'April Salary Deposit',      1, 7, 14),
  (20,  320.00, '2024-04-02', 'Dividend Income',           1, 7, 15),
  (21,  135.00, '2024-04-05', 'Costco Grocery Run',        2, 9, 16),
  (22, 1600.00, '2024-04-06', 'April Rent Payment',        2, 7, 17),
  (23,  175.00, '2024-04-10', 'Dentist Visit',             2, 9, 18),
  (24,  420.00, '2024-04-15', 'Weekend Trip to Chicago',   2, 9, 19),
  (25,   90.00, '2024-04-18', 'Meijer Grocery Run',        2, 9, 16);

--
-- Table structure for table `savings_goal`
--

DROP TABLE IF EXISTS `savings_goal`;
CREATE TABLE `savings_goal` (
  `goal_id`        INT           NOT NULL AUTO_INCREMENT,
  `goal_name`      VARCHAR(100)  NOT NULL,
  `target_amount`  DECIMAL(10,2) NOT NULL,
  `current_amount` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `target_date`    DATE          DEFAULT NULL,
  `goal_status_id` INT           NOT NULL DEFAULT 1,
  `user_id`        INT           NOT NULL,
  PRIMARY KEY (`goal_id`),
  KEY `fk_savings_goal_user_idx`        (`user_id`),
  KEY `fk_savings_goal_goal_status_idx` (`goal_status_id`),
  CONSTRAINT `fk_savings_goal_user`        FOREIGN KEY (`user_id`)        REFERENCES `user`               (`user_id`),
  CONSTRAINT `fk_savings_goal_goal_status` FOREIGN KEY (`goal_status_id`) REFERENCES `goal_status_lookup` (`goal_status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `savings_goal` VALUES
  -- goal_status_id: 1=Active, 2=Completed, 3=Cancelled
  (1,  'Emergency Fund',        5000.00,  3200.00, '2024-12-31', 1, 1),
  (2,  'New Laptop',            1500.00,   750.00, '2024-08-01', 1, 1),
  (3,  'Europe Vacation',       3000.00,  3000.00, '2024-06-01', 2, 1),
  (4,  'Emergency Fund',        4000.00,  1800.00, '2025-03-01', 1, 2),
  (5,  'Car Down Payment',      8000.00,  2500.00, '2025-06-01', 1, 2),
  (6,  'Wedding Fund',         15000.00,  4000.00, '2026-01-01', 1, 2),
  (7,  'Emergency Fund',        6000.00,  6000.00, '2024-01-01', 2, 3),
  (8,  'Home Down Payment',    25000.00,  9500.00, '2026-12-31', 1, 3),
  (9,  'New Camera Equipment',  2000.00,   800.00, '2024-10-01', 1, 3);

/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;

-- Dump completed
