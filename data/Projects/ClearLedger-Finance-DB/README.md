# ClearLedger — Personal Finance Management System

> A relational database system for tracking income, expenses, budgets, and savings goals — built in MySQL. DDP Final Project, MSIM @ UIUC.

[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql)](https://mysql.com)
[![SQL](https://img.shields.io/badge/SQL-DDL%20%2B%20DML%20%2B%20Views-orange)]()

## What It Does

ClearLedger is a normalized MySQL database that models a personal finance tracker. A user connects multiple accounts (checking, savings, credit, investment), records transactions, sets monthly budgets per category, and tracks savings goals — all queryable through a set of pre-built analytical reports.

## Schema Overview

```
user ──< account ──< transaction >── category
 │                                      │
 ├──< budget >──────────────────────────┘
 └──< savings_goal

Lookup tables: account_type · transaction_type · category_type · goal_status
```

| Table | Purpose |
|-------|---------|
| `user` | User profiles |
| `account` | Bank/financial accounts (Checking, Savings, Credit, Investment) |
| `transaction` | Income and expense records linked to accounts and categories |
| `category` | Spending/income categories (Groceries, Rent, Salary, etc.) |
| `budget` | Monthly spending limits per user per category |
| `savings_goal` | Named savings targets with progress tracking and target dates |

## File Guide

### `scripts/` — Run in numbered order

#### Setup
| File | What it does |
|------|--------------|
| `10_restore_populated_database.sql` | **Start here** — creates the `clearledger` schema, all tables, lookup data, and sample records |

#### Analytical Queries
| File | What it does |
|------|--------------|
| `11_monthly_spending_by_category.sql` | Total spent per expense category per month — spot spending trends |
| `12_monthly_income_vs_expense_summary.sql` | Month-by-month income vs. expense summary per user |
| `13_account_balance_and_activity_summary.sql` | Current balance and transaction activity per account |
| `14_budget_vs_actual.sql` | Budget limit vs. actual spend with status flags: `ON TRACK` / `Near Limit` / `OVER BUDGET` |
| `15_savings_goals_progress.sql` | Progress % and days remaining per savings goal |
| `16_full_transaction_history.sql` | Complete transaction log with category and account detail |
| `17_net_worth_summary_view.sql` | Creates a reusable `net_worth_summary_view` — total income, expenses, net cash flow, account balance |

#### CRUD Operations
| File | What it does |
|------|--------------|
| `50_add_a_new_transaction.sql` | INSERT a new income or expense transaction |
| `51_edit_a_transaction.sql` | UPDATE an existing transaction's amount, date, or description |
| `52_delete_a_transaction.sql` | DELETE a transaction by ID |
| `53_add_a_new_account.sql` | INSERT a new financial account for a user |
| `54_delete_an_account.sql` | DELETE an account (cascades to transactions) |
| `55_add_a_new_budget.sql` | INSERT a monthly budget limit for a category |
| `56_update_a_budget.sql` | UPDATE a budget's monthly limit |
| `57_add_a_new_savings_goal.sql` | INSERT a new savings goal with target amount and date |
| `58_complete_a_savings_goal.sql` | Mark a savings goal as completed |
| `59_add_a_new_category.sql` | INSERT a new spending or income category |
| `60_delete_a_category.sql` | DELETE a category |

### `documentation/`
| File | What it does |
|------|--------------|
| `database_schema_erd.pdf` | Entity-Relationship Diagram — full schema with cardinalities |
| `system_prototype_description.pdf` | System design document: scope, use cases, design decisions |

## How to Run

```sql
-- 1. Restore schema + sample data
SOURCE scripts/10_restore_populated_database.sql;

-- 2. Run any analytical query, e.g. budget vs. actual
SOURCE scripts/14_budget_vs_actual.sql;

-- 3. Try a CRUD operation, e.g. add a transaction
SOURCE scripts/50_add_a_new_transaction.sql;
```

**Requirements:** MySQL 8.0+, MySQL Workbench or any MySQL client.

## Design Highlights

- **Lookup tables** for account type, transaction type, category type, and goal status — avoids magic numbers and makes joins self-documenting
- **Reusable VIEW** (`net_worth_summary_view`) for the top-level financial health snapshot
- **Budget status logic** built into SQL using `CASE WHEN` — no application layer needed
- **`COALESCE`** throughout to handle users with no transactions gracefully
- Sample data scoped to realistic personal finance scenarios (groceries, rent, salary, savings goals)

## Context

Final project for the **Database Design Prototyping (DDP)**, Master of Science in Information Management (MSIM), University of Illinois Urbana-Champaign.
